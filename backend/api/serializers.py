from api.utils import Base64ImageField
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from djoser.serializers import UserSerializer

from users.models import Subscription
from recipes.models import (Favorite, Ingredient, IngredientRecipes, Recipe,
                            ShoppingCart, Tag)

User = get_user_model()


class UserSerializer(UserSerializer):
    '''
    Сериалайзер для модели User.
    Используется для отображения базовой информации о пользователе
    '''
    is_subscribed = SerializerMethodField()

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'

        )
        model = User

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user is None or user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=user,
            author=obj
        ).exists()


class IngredientSerializer(serializers.ModelSerializer):
    '''Сериалайзер для модели Ingredient.'''
    class Meta:
        fields = '__all__'
        model = Ingredient


class IngredientRecipeReadSerializer(serializers.ModelSerializer):
    '''
    Сериалайзер для модели IngredientRecipes.
    Используется для коректного отображения полей ингредиента при чтении.
    '''
    id = serializers.IntegerField(source='ingredient.id')
    name = serializers.CharField(source='ingredient.name')
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
        )

    class Meta:
        fields = ('id', 'name', 'amount', 'measurement_unit')
        model = IngredientRecipes


class IngredientRecipeWriteSerializer(serializers.ModelSerializer):
    '''
    Сериалайзер для модели IngredientRecipes.
    Используется для коректного отображения рецепта при записи.
    '''
    id = serializers.IntegerField()

    class Meta:
        fields = ('id', 'amount')
        model = IngredientRecipes


class TagSerializer(serializers.ModelSerializer):
    '''
    Сериалайзер для модели Tag.
    '''
    class Meta:
        fields = '__all__'
        model = Tag


class RecipeReadSerializer(serializers.ModelSerializer):
    '''
    Сериалайзер для модели Recipe.
    Используется на отображение необходимых полей при чтеннии.
    '''
    tags = TagSerializer(many=True, read_only=True)
    author = UserSerializer()
    image = Base64ImageField()
    ingredients = IngredientRecipeReadSerializer(
        many=True, source='amount_ingredients'
        )
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        model = Recipe

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorites.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.cart.filter(recipe=obj).exists()


class RecipeWriteSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для модели Recipe.
    Используется для записи рецепта.
    '''
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeWriteSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        model = Recipe

    def create_ingredients(self, ingredients, recipe):
        for ingredient in ingredients:
            ingredients, status = IngredientRecipes.objects.get_or_create(
                recipe=recipe,
                ingredient=Ingredient.objects.get(id=ingredient['id']),
                amount=ingredient['amount']
            )

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(recipe=recipe, ingredients=ingredients)
        return recipe

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance = super(RecipeWriteSerializer, self).update(instance,
                                                             validated_data)
        instance.tags.set(tags)
        self.create_ingredients(recipe=instance, ingredients=ingredients)
        instance.save()
        return instance

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadSerializer(instance,
                                    context=context).data


class RecipeFavoriteSerializer(serializers.ModelSerializer):
    '''
    Сериализатор работает с моделью Recipe.
    Используется для отображения ответа при добавлении рецепта в избранное.
    '''
    class Meta:
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )
        model = Recipe


class FavoriteSerializer(serializers.ModelSerializer):
    '''
    Сериализатор работает с моделью Favorite.
    Испльзуется для создание связей избранных рецептов пользователя.
    '''
    class Meta:
        fields = (
            'user',
            'recipe'
        )
        model = Favorite


class ShoppingCartSerializer(serializers.ModelSerializer):
    '''
    Сериализатор работает с моделью ShoppingCart.
    Используется для формирования карзины покупок пользователя.
    '''
    class Meta:
        fields = (
            'user',
            'recipe'
        )
        model = ShoppingCart


class SubscriptionSerializer(serializers.ModelSerializer):
    '''
    Сериализатор работает с моделью Subscription.
    Используется на запись при подписке на пользователя.
    '''
    class Meta:
        fields = (
            'user',
            'author'
        )
        model = Subscription


class SubscriptionReadSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для модели User.
    Используется на отображение необходимых полей при подписке
    '''
    is_subscribed = SerializerMethodField()
    recipes = RecipeFavoriteSerializer(many=True)
    recipes_count = SerializerMethodField()

    class Meta:
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes',
            'recipes_count'
        )
        model = User

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user is None or user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=user,
            author=obj
        ).exists()

    def get_recipes_count(self, obj):
        return obj.recipes.count()
