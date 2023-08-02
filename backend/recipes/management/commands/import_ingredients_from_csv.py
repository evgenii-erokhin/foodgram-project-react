import csv

from django.conf import settings
from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open(f'{settings.BASE_DIR}/data/ingredients.csv',
                  'r',
                  encoding='utf-8') as f:
            reader = csv.DictReader(f)
            Ingredient.objects.bulk_create(
                Ingredient(**row) for row in reader
            )

        self.stdout.write(self.style.SUCCESS('Ингредиенты успешно загруженны'))
