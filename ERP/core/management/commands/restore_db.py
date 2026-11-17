"""
Restore the database from a backup. STOP THE ERP SERVICE FIRST.

    python manage.py restore_db backups\erp-20261117-020000.sqlite3 --yes

The current database is saved as db.before-restore-<time>.sqlite3 first.
"""
from django.core.management.base import BaseCommand, CommandError

from core import automation


class Command(BaseCommand):
    help = 'Restore the database from a backup file (stop the ERP service first).'

    def add_arguments(self, parser):
        parser.add_argument('backup_file')
        parser.add_argument('--yes', action='store_true', help='Confirm: replace the live database.')

    def handle(self, *args, backup_file, yes, **options):
        if not yes:
            raise CommandError('This REPLACES the live database. Stop the ERP service, then re-run with --yes.')
        try:
            r = automation.restore_database(backup_file)
        except ValueError as e:
            raise CommandError(str(e))
        self.stdout.write(self.style.SUCCESS(
            f"Restored from {r['restored_from']}. Previous database saved as {r['safety_copy']}."))
