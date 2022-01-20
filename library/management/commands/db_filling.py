from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'The command allows you to fill the database with test data'

    def handle(self, *args, **options):
        from library.services.command_services import DatabaseStuffer
        DatabaseStuffer().fill()
