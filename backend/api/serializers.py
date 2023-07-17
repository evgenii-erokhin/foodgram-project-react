from rest_framework import serializers
from django.db.models import F
from rest_framework.fields import SerializerMethodField
from recipes.models import Recipe, Tag, Ingredient, IngredientRecipes


class IngredientSerializers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class IngredientRecipesSerializers(serializers.ModelSerializer):
    class Meta:
        model = IngredientRecipes
        fields = '__all__'


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag


class RecipeSerializers(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='first_name'
    )
    tags = TagSerializers(many=True, read_only=True)
    ingredients = SerializerMethodField()

    class Meta:
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favourite',
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
