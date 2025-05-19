from django.core.management.base import BaseCommand
from users.models import Role

class Command(BaseCommand):
    help = 'Seed roles data'

    def handle(self, *args, **kwargs):
        roles = ['administrator', 'manager', 'cashier', 'customer']

        for role_type in roles:
            _, created = Role.objects.get_or_create(role_type=role_type)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Role "{role_type}" created'))
            else:
                self.stdout.write(f'Role "{role_type}" already exists')

        self.stdout.write(self.style.SUCCESS('Roles seeding complete!'))