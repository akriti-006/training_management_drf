# core/management/commands/create_groups.py

from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

# Import all relevant models
from shared_app.models import ProgrammingLanguage, Framework, CourseData, TrainingEnquery, CourseEnrollment, FeeInformation, CourseEnrollmentExtensionLog


class Command(BaseCommand):
    help = 'Create user groups and assign relevant permissions'

    def handle(self, *args, **kwargs):
        group_names = ['Admin', 'HR', 'Student', 'Teacher']
        groups = {}

        # Create groups if not already created
        for name in group_names:
            group, created = Group.objects.get_or_create(name=name)
            groups[name] = group
            if created:
                self.stdout.write(self.style.SUCCESS(f'Group "{name}" created.'))
            else:
                self.stdout.write(self.style.WARNING(f'Group "{name}" already exists.'))

        # Assign permissions to Admin and HR
        models = [ProgrammingLanguage, Framework, CourseData, TrainingEnquery,
                  CourseEnrollment, FeeInformation, CourseEnrollmentExtensionLog]

        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type)
            groups['Admin'].permissions.add(*permissions)
            groups['HR'].permissions.add(*permissions)

        # Assign limited permissions to Teacher group
        course_ct = ContentType.objects.get_for_model(CourseData)
        try:
            change_perm = Permission.objects.get(codename='change_coursedata', content_type=course_ct)
            groups['Teacher'].permissions.add(change_perm)
        except Permission.DoesNotExist:
            self.stdout.write(self.style.ERROR('change_coursedata permission not found'))

        self.stdout.write(self.style.SUCCESS('Groups and permissions assignment completed.'))

