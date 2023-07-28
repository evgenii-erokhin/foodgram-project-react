from django.core.validators import MinValueValidator, RegexValidator
from django.db import models

from users.models import User


class Ingredient(models.Model):
    '''Модель ингредиента'''
    name = models.CharField(
        'Название ингридиента',
        max_length=200,
    )
    measurement_unit = models.CharField(
        'Еденицы измерения',
        max_length=200,
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        ordering = ['name']

    def __str__(self):
        return f'{self.name} - {self.measurement_unit}'


class Tag(models.Model):
    '''Модель Тега'''
    name = models.CharField(
        'Название тега',
        max_length=200,
        unique=True,
    )
    color = models.CharField(
        'Цвет Тега',
        max_length=7,
        unique=True,
        validators=[RegexValidator(
            '^#([a-fA-F0-9]{6})',
            message='Цвет тега должен быть указан в hex формате')]
    )
    slug = models.SlugField(
        'Уникальный слаг',
        max_length=200,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']

    def __str__(self):
        return self.name


class Recipe(models.Model):
    '''Модель рецепта'''
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        'Название рецепта',
        max_length=200
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/images',
    )
    text = models.TextField(
        'Описание',
        max_length=1000,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='IngredientRecipes',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        verbose_name='Теги'
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=[MinValueValidator
                    (1, 'Время приготовления должно быть'
                     'равно хотя бы одной минуте')]
    )
    pub_date = models.DateTimeField(
        'Дата и время публикации рецепта',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class IngredientRecipes(models.Model):
    '''Промежуточная модель для связи ингридиента и рецепта'''
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='amount_ingredients',
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        related_name='amount_ingredients',
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        'Количество',
        validators=[MinValueValidator
                    (1, 'Количество должно быть равно хотя бы одному')]
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique_ingredient'
            )
        ]
        ordering = ['recipe']

    def __str__(self):
        return (f'{self.ingredient.name}, {self.amount}'
                f'{self.ingredient.measurement_unit}')


class Favorite(models.Model):
    '''Модель для избранных рецептов'''
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favourites'
            )
        ]
        ordering = ['user']

    def __str__(self):
        return f'{self.user} добавил в избранное {self.recipe}'


class ShoppingCart(models.Model):
    '''Модель корзины покупок'''
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='cart',
        verbose_name='Рецепт'
    )

    class Meta:
        verbose_name = 'Корзина покупок'
        verbose_name_plural = 'Корзина покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart'
            )
        ]
        ordering = ['user']

    def __str__(self):
        return f'{self.user} добавил {self.recipe} в корзину покупок '
