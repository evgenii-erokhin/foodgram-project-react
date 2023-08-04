from django.forms import BaseInlineFormSet


class IngredientRecipeForm(BaseInlineFormSet):
    def _construct_form(self, i, kwargs):
        form = super(IngredientRecipeForm, self)._construct_form(i, kwargs)
        if i < 1:
            form.empty_permitted = False
        return form
