from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from djoser.views import UserViewSet
from recipes.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             RecipeFavoriteSerializer, RecipeReadSerializer,
                             RecipeWriteSerializer, ShoppingCartSerializer,
                             SubscriptionReadSerializer,
                             SubscriptionSerializer, TagSerializer,
                             UserSerializer)
from users.models import Subscription

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
    '''
    Вьюсет для работы с рецептами.
    Позволяет добавять/удалять рецепты в "Избранное"
    и в "Корзину покупок".
    '''
    pagination_class = PageNumberPagination

    def get_queryset(self):
        recipes = Recipe.objects.prefetch_related(
            'amount_ingredients__ingredient', 'tags'
        ).all()
        return recipes

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk):
        '''
        Метод "favorite" позволяет текущему пользователю
        в зависимости от метода запроса добавить/удалить
        рецепт в список "Избранное".
        '''
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':
            serializer = FavoriteSerializer(
                data={'user': user.id, 'recipe': recipe.id})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            fav_recipe_serializer = RecipeFavoriteSerializer(recipe)
            return Response(
                fav_recipe_serializer.data,
                status=status.HTTP_201_CREATED
            )

        favorite_recipe = get_object_or_404(
            Favorite, user=user, recipe=recipe)
        favorite_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk):
        '''
        Метод "shopping_cart" позволяет текущему пользователю
        в зависимости от запроса добавить/удалить ингредиенты
        рецепта в "Корзину покупок".
        '''
        user = request.user
        recipe = get_object_or_404(Recipe, id=pk)

        if request.method == 'POST':
            serializer = ShoppingCartSerializer(
                data={'user': user.id, 'recipe': recipe.id}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            shopping_cart_serializer = RecipeFavoriteSerializer(recipe)
            return Response(
                shopping_cart_serializer.data,
                status=status.HTTP_201_CREATED
            )

        shopping_cart = get_object_or_404(
            ShoppingCart, user=user, recipe=recipe)
        shopping_cart.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ModelViewSet):
    '''Вьюсет для работы с тегами'''
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    '''Вьюсет для работы с ингредиентами'''
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True,  methods=['post', 'delete'])
    def subscribe(self, request, id):
        '''
        Метод "subscribe" позволяет текущему пользователю
        подписаться/отписаться на автора рецепта.
        '''
        user = request.user
        author = get_object_or_404(User, id=id)
        if request.method == 'POST':
            serializer = SubscriptionSerializer(
                data={
                    'user': user.id,
                    'author': author.id
                }
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            subscribe_serializer = SubscriptionReadSerializer(
                author,
                context={'request': request}

            )
            return Response(
                subscribe_serializer.data,
                status=status.HTTP_201_CREATED)
        subscribe_serializer = get_object_or_404(
            Subscription,
            user=user,
            author=author
            )
        subscribe_serializer.delete()
        return Response(
            status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def subscriptions(self, request):
        '''
        Метод "subscriptions" возвращает пользователей,
        на которых подписан текущий пользователь.
        В выдачу добавляются рецепты.
        '''
        user = request.user
        authors = User.objects.filter(subscribing__user=user)

        paged_queryset = self.paginate_queryset(authors)
        serializer = SubscriptionReadSerializer(
            paged_queryset,
            context={'request': request},
            many=True
        )
        return self.get_paginated_response(serializer.data)
