from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Create default user groups: Admin, HR, Student, Teacher'

    def handle(self, *args, **kwargs):
        group_names = ['Admin', 'HR', 'Student', 'Teacher']
        for name in group_names:
            group, created = Group.objects.get_or_create(name=name)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Group "{name}" created.'))
            else:
                self.stdout.write(self.style.WARNING(f'Group "{name}" already exists.'))
