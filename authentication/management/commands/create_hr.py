from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()  # ✅ This gets your custom User model

class Command(BaseCommand):
    help = 'Create HR profile with predefined credentials'

    def handle(self, *args, **kwargs):
        email = 'akritisharma4111@gmail.com'
        password = 'aksharma'
        first_name = 'Akriti'
        last_name = 'Sharma'
        username = email  # Assuming username = email

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'User with email "{email}" already exists.'))
            return

        user = User.objects.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            is_staff=True
        )

        # Assign to HR group
        hr_group, _ = Group.objects.get_or_create(name='HR')
        user.groups.add(hr_group)

        self.stdout.write(self.style.SUCCESS(f'HR user "{email}" created and added to "HR" group.'))
