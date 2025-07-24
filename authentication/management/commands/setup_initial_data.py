from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Runs initial setup: creates HR, Admin, and Groups'

    def handle(self, *args, **kwargs):
        try:

            self.stdout.write(self.style.NOTICE('Running create_group...'))
            call_command('create_groups')
            
            self.stdout.write(self.style.NOTICE('Running create_admin...'))
            call_command('create_admin')

            self.stdout.write(self.style.NOTICE('Running create_hr...'))
            call_command('create_hr')

            self.stdout.write(self.style.SUCCESS('All setup commands ran successfully!'))

        except CommandError as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
