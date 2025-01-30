from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Override the staticfiles storage and run collectstatic'

    def handle(self, *args, **options):
        # Override the STATICFILES_STORAGE setting dynamically
        settings.STATICFILES_STORAGE = 'custom_storages.StaticStorage'
        # Run the collectstatic command
        call_command('collectstatic', *args, **options)