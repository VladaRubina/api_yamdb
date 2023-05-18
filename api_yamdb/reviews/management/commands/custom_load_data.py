import csv

from django.core.management.base import BaseCommand
from reviews.models import Category


class Command(BaseCommand):
    help = 'Загрузка данных.'

    # def add_arguments(self, parser: CommandParser) -> None:
    #     parser.add_argument('data', nargs='+', type=str)

    def handle(self, *args, **options):
        csv_file1 = 'static/data/category.csv'
        # for file_path in csv_files:
        #     if
        with open(csv_file1, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # print(count(row))
                # key = (1, 2, 3,..)
                # len(key)
                Category.objects.create(
                    id=row['id'], name=row['name'], slug=row['slug']
                )
