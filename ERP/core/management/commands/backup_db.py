"""Back up the database now:  python manage.py backup_db"""
from django.core.management.base import BaseCommand, CommandError

from core import automation


class Command(BaseCommand):
    help = 'Create a verified backup of the database and uploaded files now.'

    def handle(self, *args, **options):
        r = automation.backup_database()
        if not r['ok']:
            raise CommandError(r['message'])
        self.stdout.write(self.style.SUCCESS(r['message']))
