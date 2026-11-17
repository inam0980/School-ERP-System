"""Run all nightly automation jobs. Scheduled by deploy/install_daily_jobs.bat."""
from django.core.management.base import BaseCommand

from core import automation


class Command(BaseCommand):
    help = 'Nightly jobs: backup, fee statuses, staff compliance, (optional) reminders, admin email.'

    def handle(self, *args, **options):
        results = automation.run_daily_jobs()
        failed = [n for n, r in results.items() if not r.get('ok')]
        for name, r in results.items():
            line = f"[{'OK' if r.get('ok') else 'FAILED'}] {name}: {r.get('message', '')}"
            self.stdout.write(self.style.SUCCESS(line) if r.get('ok') else self.style.ERROR(line))
        if failed:
            raise SystemExit(1)       # non-zero exit so Task Scheduler shows the failure
