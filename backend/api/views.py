from api.serializers import (FavoriteSerializer, IngredientSerializer,
                             RecipeFavoriteSerializer, RecipeReadSerializer,
                             RecipeWriteSerializer, ShoppingCartSerializer,
                             SubscriptionReadSerializer,
                             SubscriptionSerializer, TagSerializer,
                             UserSerializer)
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from recipes.models import (Favorite, Ingredient, Recipe, ShoppingCart, Tag)
from users.models import Subscription
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response

User = get_user_model()


class RecipeViewSet(viewsets.ModelViewSet):
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
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=['post', 'delete'])
    def subscribe(self, request, pk):
        user = request.user
        author = get_object_or_404(User, id=pk)
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

    @action(detail=True, methods=['get'])
    def subscriptions(self, request):
        user = request.user
        authors = User.objects.filter(subscriber=user)
        return print(authors)

    @action(detail=False, url_path='me', url_name='me')
    def get_me_page(self, request):
        # UserSerializer
        user = request.user
        serializer = UserSerializer(
            user, context={'request': request}
        )
        return Response(serializer.data)
