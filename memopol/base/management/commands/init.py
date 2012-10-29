from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Initialize project'

    def handle(self, *args, **options):
        call_command("syncdb", interactive=False)
        call_command("migrate", "categories")
        call_command("migrate", "reps", "0007")
        call_command("migrate", "meps")
        call_command("migrate")
        call_command("rebuild_index", interactive=False)
        if settings.get("COMPRESS_OFFLINE", False):
            call_command("compress")
