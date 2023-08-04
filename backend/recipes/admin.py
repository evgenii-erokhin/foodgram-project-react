from django.contrib import admin
from django import forms
from recipes.models import (Favorite, Ingredient, IngredientRecipes, Recipe,
                            ShoppingCart, Tag)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name', )


class UserForm(forms.Form):
    name = forms.CharField()
    amount = forms.IntegerField()


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipes
    form = UserForm


class TagInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 0
    min_num = 1


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
