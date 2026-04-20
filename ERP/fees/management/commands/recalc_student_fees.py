"""
Management command: recalc_student_fees
Usage: python manage.py recalc_student_fees [--dry-run]

Recalculates net_amount for every StudentFee record based on the student's
current is_saudi flag and the fee type's VAT rate.  Run this whenever a
student's id_type (Saudi / Iqama / Passport) is corrected.
"""
from decimal import Decimal

from django.core.management.base import BaseCommand

from fees.models import StudentFee


class Command(BaseCommand):
    help = 'Recalculate net_amount for all StudentFee records (fixes wrong VAT)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run', action='store_true',
            help='Show what would change without saving',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        fixed = skipped = 0

        qs = StudentFee.objects.select_related('student', 'fee_structure__fee_type')
        for f in qs.iterator():
            base = f.amount - f.discount
            if base < 0:
                base = Decimal('0.00')
            rate = f.fee_structure.fee_type.vat_rate_for(f.student.is_saudi)
            expected = (base * (1 + rate)).quantize(Decimal('0.01'))
            if expected != f.net_amount:
                msg = (
                    f'  {"[DRY]" if dry_run else "FIXED"} pk={f.pk} '
                    f'{f.student.full_name} ({f.fee_structure.fee_type.name}): '
                    f'{f.net_amount} → {expected}'
                )
                self.stdout.write(msg)
                if not dry_run:
                    f.save()
                fixed += 1
            else:
                skipped += 1

        style = self.style.WARNING if dry_run else self.style.SUCCESS
        self.stdout.write(style(
            f'\nDone. {"Would fix" if dry_run else "Fixed"} {fixed} records, '
            f'{skipped} already correct.'
        ))
