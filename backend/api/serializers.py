
from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.validators import UniqueTogetherValidator

from recipes.models import (Favorite, Ingredient, IngredientRecipes, Recipe,
                            ShoppingCart, Tag)
from users.models import Subscription

User = get_user_model()


class UserSerializer(UserSerializer):
    '''
    Сериалайзер для модели User.
    Используется для отображения базовой информации о пользователе
    '''
    is_subscribed = SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, obj):
        '''
        Проверяет подписан ли текущий пользователь на автора
        '''
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
        model = Ingredient
        fields = (
            'name',
            'measurement_unit'
        )


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
        model = IngredientRecipes
        fields = (
            'id',
            'name',
            'amount',
            'measurement_unit'
        )


class IngredientRecipeWriteSerializer(serializers.ModelSerializer):
    '''
    Сериалайзер для модели IngredientRecipes.
    Используется для коректного отображения рецепта при записи.
    '''
    id = serializers.IntegerField()

    class Meta:
        model = IngredientRecipes
        fields = (
            'id',
            'amount'
        )


class TagSerializer(serializers.ModelSerializer):
    '''
    Сериалайзер для модели Tag.
    '''
    class Meta:
        model = Tag
        fields = (
            'name',
            'color',
            'slug'
        )


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
        model = Recipe
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

    def get_is_favorited(self, obj):
        user = self.context.get('request').user
        return (user.is_authenticated and
                user.favorites.filter(recipe=obj).exists())

    def get_is_in_shopping_cart(self, obj):
        user = self.context.get('request').user
        return (user.is_authenticated and
                user.cart.filter(recipe=obj).exists())


class RecipeWriteSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для модели Recipe.
    Используется для записи рецепта.
    '''
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    author = UserSerializer(read_only=True)
    ingredients = IngredientRecipeWriteSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
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

    def create_ingredients(self, ingredients, recipe):
        '''Метод создания ингредиентов с количеством ингредиентов.'''
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
        model = Recipe
        fields = (
            'id',
            'name',
            'image',
            'cooking_time'
        )


class FavoriteSerializer(serializers.ModelSerializer):
    '''
    Сериализатор работает с моделью Favorite.
    Испльзуется для создание связей избранных рецептов пользователя.
    '''
    class Meta:
        model = Favorite
        fields = (
            'user',
            'recipe'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Favorite.objects.all(),
                fields=['user', 'recipe'],
                message='Вы уже добавили этот рецепт в избранное'
            )
        ]


class ShoppingCartSerializer(serializers.ModelSerializer):
    '''
    Сериализатор работает с моделью ShoppingCart.
    Используется для формирования карзины покупок пользователя.
    '''
    class Meta:
        model = ShoppingCart
        fields = (
            'user',
            'recipe'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=ShoppingCart.objects.all(),
                fields=['user', 'recipe'],
                message='Вы уже добавили этот рецепт в корзину покупок'
            )
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    '''
    Сериализатор работает с моделью Subscription.
    Используется на запись при подписке на пользователя.
    '''
    class Meta:
        model = Subscription
        fields = (
            'user',
            'author'
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Subscription.objects.all(),
                fields=['user', 'author'],
                message='Дважды на одного пользователя нельзя подписаться'
            )
        ]

    def validate(self, data):
        if data['author'] == data['user']:
            raise serializers.ValidationError('Нельзя подписаться на себя')
        return data


class SubscriptionReadSerializer(serializers.ModelSerializer):
    '''
    Сериализатор для модели User.
    Используется на отображение необходимых полей при подписке
    '''
    is_subscribed = SerializerMethodField()
    recipes = RecipeFavoriteSerializer(many=True)
    recipes_count = SerializerMethodField()

    class Meta:
        model = User
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

    def get_is_subscribed(self, obj):
        '''
        Метод который возвращает булево значение,
        которое показывает подписан ли полльзователь на автора рецепта.
        '''
        user = self.context.get('request').user
        if user is None or user.is_anonymous:
            return False
        return Subscription.objects.filter(
            user=user,
            author=obj
        ).exists()

    def get_recipes_count(self, obj):
        '''Метод возвращает количество рецептов у автора рецептов
          на которого подписался пользователь.
          '''
        return obj.recipes.count()
