from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Initialize project'

    def handle(self, *args, **options):
        call_command("syncdb", interactive=False)
        call_command("migrate")
        call_command("rebuild_index", interactive=False)
        if hasattr(settings, "COMPRESS_OFFLINE") and settings.COMPRESS_OFFLINE:
            call_command("compress")
