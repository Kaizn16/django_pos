from django.core.management.base import BaseCommand
from products.models import Category

class Command(BaseCommand):
    help = 'Seed food categories data'

    def handle(self, *args, **kwargs):
        categories = [
            'Beverages',
            'Snacks',
            'Canned & Jarred Goods'
        ]

        for category_name in categories:
            _, created = Category.objects.get_or_create(category_name=category_name, parent=None)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Category "{category_name}" created'))
            else:
                self.stdout.write(f'Category "{category_name}" already exists')

        self.stdout.write(self.style.SUCCESS('Food category seeding complete!'))