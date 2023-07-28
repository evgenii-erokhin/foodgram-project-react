import csv

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):

    def handle(self, *args, **options):
        with open('D:/Dev/foodgram-project-react/data/ingredients.csv',
                  'r',
                  encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                Ingredient.objects.create(
                    name=row[0],
                    measurement_unit=row[1]
                )
        self.stdout.write(self.style.SUCCESS('Ингредиенты успешно загруженны'))
