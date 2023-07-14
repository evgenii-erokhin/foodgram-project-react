from django.db import models
from django.core.validators import MinValueValidator

from users.models import User


class Ingrediet(models.Model):
    '''Модель ингредиента'''
    name = models.CharField(
        'Название ингридиента',
        max_length=200,
        blank=False
        )
    measurement_unit = models.CharField(
        'Еденицы измерения',
        max_length=200,
        blank=False
    )

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

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
        unique=True
    )
    slug = models.SlugField(
        'Уникальный слаг',
        max_length=200,
        unique=True
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

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
    )
    image = models.ImageField(
        'Изображение',
        upload_to='recipes/',
    )
    text = models.TextField(
        'Описание',
        max_length=1000,
    )
    ingrediets = models.ManyToManyField(
        Ingrediet,
        through='IngredietRecipes',
        related_name='recipes',
        verbose_name='Ингредиенты'
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tags',
        verbose_name='Теги'
    )
    cooking_time = models.PositiveIntegerField(
        'Время приготовления',
        validators=[MinValueValidator
                    (1, 'Время приготовления должно быть'
                     'равно хотя бы одной минуте')]
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.text


class IngredietRecipes(models.Model):
    '''Промежуточная модель для связи ингридиента и рецепта'''

    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    ingredient = models.ForeignKey(
        Ingrediet,
        on_delete=models.CASCADE,
        related_name='ingredients'
    )
    amount = models.PositiveIntegerField(
        'Количество',
        validators=[MinValueValidator
                    (1, 'Количество должно быть равно хотя бы одному')]
    )

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'


class Favorit(models.Model):
    ...


class ShopingList(models.Model):
    ...
