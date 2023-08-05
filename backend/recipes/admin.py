from django.contrib import admin
from recipes.forms import NotAllowEmtyForm
from recipes.models import (Favorite, Ingredient, IngredientRecipes, Recipe,
                            ShoppingCart, Tag)


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name', )


class IngredientRecipeInline(admin.TabularInline):
    model = IngredientRecipes
    extra = 0
    min_num = 1
    formset = NotAllowEmtyForm


class TagInline(admin.TabularInline):
    model = Recipe.tags.through
    extra = 0
    min_num = 1
    formset = NotAllowEmtyForm


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
