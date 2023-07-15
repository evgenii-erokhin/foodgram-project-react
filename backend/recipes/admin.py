from django.contrib import admin
from recipes.models import (Favourite, Ingrediet, IngredietRecipes, Recipe,
                            ShoppingCart, Tag)


class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class IngredietAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit')
    list_filter = ('name', )


class IngredietRecipesAdmin(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount')


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'author')
    list_filter = ('author', 'name', 'tags')


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe')


class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug')


admin.site.register(Favourite, FavouriteAdmin)
admin.site.register(Ingrediet, IngredietAdmin)
admin.site.register(IngredietRecipes, IngredietRecipesAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(ShoppingCart, ShoppingCartAdmin)
admin.site.register(Tag, TagAdmin)
