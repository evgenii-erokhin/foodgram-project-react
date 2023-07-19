from django.db.models import F
from recipes.models import Ingredient, IngredientRecipes, Recipe, Tag
from rest_framework import serializers
from rest_framework.fields import IntegerField, SerializerMethodField

from api.utils import Base64ImageField


class IngredientSerializers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class IngredientRecipeSerializers(serializers.ModelSerializer):
    id = IntegerField()

    class Meta:
        fields = ('id', 'amount')
        model = IngredientRecipes


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class RecipeReadSerializers(serializers.ModelSerializer):
    tags = TagSerializers(many=True, read_only=True)
    image = Base64ImageField()
    ingredients = SerializerMethodField()

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

    def get_ingredients(self, obj):
        recipe = obj
        ingredients = recipe.ingredients.values(
            'id',
            'name',
            'measurement_unit',
            amount=F('amount_ingredients__amount')
        )
        return ingredients


class RecipeWriteSerializers(serializers.ModelSerializer):
    tags = serializers.PrimaryKeyRelatedField(queryset=Tag.objects.all(),
                                              many=True)
    ingredients = IngredientRecipeSerializers(many=True)
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

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeReadSerializers(instance,
                                     context=context).data
