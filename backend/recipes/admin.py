from django.contrib import admin
from django.forms import ValidationError
from recipes.models import (Favorite, Ingredient, IngredientRecipes, Recipe,
                            ShoppingCart, Tag)
from django.forms.models import BaseInlineFormSet


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name', )


class PageFormSet(BaseInlineFormSet):

    def clean(self):
        super(PageFormSet, self).clean()

        for form in self.forms:
            if not hasattr(form, 'cleaned_data'):
                continue

            data = form.cleaned_data
            curr_instance = form.instance
            was_read = curr_instance.was_read

            if (data.get('DELETE') and was_read):
                raise ValidationError('Error')


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipes
    min_num = 1
    extra = 0


class TagInline(admin.TabularInline):
    model = Recipe.tags.through
    min_num = 1
    extra = 0


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author', 'pub_date')
    list_filter = ('author', 'name', 'tags')
    exclude = ('tags',)
    inlines = [IngredientRecipeInline, TagInline]


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
