from django import forms

from recipes.models import IngredientRecipes


class IngredientRecipeForm(forms.ModelForm):
    class Meta:
        model = IngredientRecipes
        fields = (
            'ingredient',
            'amount'
        )
