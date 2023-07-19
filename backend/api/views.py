from api.serializers import (RecipeReadSerializers, RecipeWriteSerializers,
                             TagSerializers, IngredientSerializers)
from recipes.models import Recipe, Tag, Ingredient
from rest_framework import viewsets
from rest_framework.permissions import SAFE_METHODS


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializers
        return RecipeWriteSerializers


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializers


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializers
