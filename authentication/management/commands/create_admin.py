from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

class Command(BaseCommand):
    help = 'Create Admin profile with predefined credentials'

    def handle(self, *args, **kwargs):
        email = 'admin@gmail.com'
        password = 'admin'
        first_name = 'admin'
        last_name = 'admin'
        username = email  # Assuming username = email

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User with username "{username}" already exists.'))
            return

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True,
            is_superuser=True
        )

        # Assign to HR group
        hr_group, _ = Group.objects.get_or_create(name='Admin')
        user.groups.add(hr_group)

        self.stdout.write(self.style.SUCCESS(f'Admin user "{username}" created and added to "Admin" group.'))
