from django.core.management.base import BaseCommand
from sales.models import Discount

class Command(BaseCommand):
    help = 'Seed initial discount records'

    def handle(self, *args, **kwargs):
        initial_discounts = [
            {'name': 'PWD Discount', 'percentage': 20.00},
            {'name': 'Senior Citizen Discount', 'percentage': 15.00},
            {'name': 'Student Discount', 'percentage': 10.00},
            {'name': 'Holiday Sale Discount', 'percentage': 25.00},
            {'name': 'Loyalty Member Discount', 'percentage': 10.00},
            {'name': 'New Customer Discount', 'percentage': 15.00},
        ]

        for discount_data in initial_discounts:
            discount, created = Discount.objects.get_or_create(
                name=discount_data['name'],
                defaults={
                    'percentage': discount_data['percentage'],
                    'active': True
                }
            )

            if created:
                self.stdout.write(self.style.SUCCESS(f'Created discount: "{discount.name}"'))
            else:
                self.stdout.write(f'Discount already exists: "{discount.name}"')

        self.stdout.write(self.style.SUCCESS('Discount seeding completed successfully.'))
