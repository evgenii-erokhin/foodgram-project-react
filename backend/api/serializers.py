from rest_framework import serializers

from recipes.models import Recipe, Tag, Ingredient


class IngredientSerializers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Ingredient


class RecipeSerializers(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='first_name'
    )

    class Meta:
        fields = '__all__'
        model = Recipe


class TagSerializers(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = Tag
