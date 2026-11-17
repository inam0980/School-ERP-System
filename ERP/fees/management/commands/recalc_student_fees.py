"""
Management command: recalc_student_fees

    python manage.py recalc_student_fees --dry-run        # show what would change
    python manage.py recalc_student_fees                  # re-price fees with NO payments
    python manage.py recalc_student_fees --include-paid   # also re-price fees already (part-)paid

Recalculates StudentFee.net_amount from the student's current is_saudi flag and
the fee type's VAT rate. Run it after a student's id_type (Saudi / Iqama /
Passport) has been corrected (see `fix_student_id_types`).

Safety (decided 2026-11-17):
- Fees that already have payments are skipped unless --include-paid is given:
  re-billing a settled fee is a finance decision.
- Every re-priced fee gets its status refreshed, so a fully paid fee whose
  price went up becomes PARTIAL instead of staying PAID with a balance.
"""
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from fees.models import StudentFee


class Command(BaseCommand):
    help = 'Recalculate net_amount for StudentFee records (fixes wrong VAT). Skips paid fees by default.'

    def add_arguments(self, parser):
        parser.add_argument('--dry-run', action='store_true', help='Show what would change without saving')
        parser.add_argument('--include-paid', action='store_true',
                            help='Also re-price fees that already have payments (finance approval needed)')

    def handle(self, *args, **options):
        dry_run, include_paid = options['dry_run'], options['include_paid']
        fixed = correct = skipped_paid = 0

        qs = StudentFee.objects.select_related('student', 'fee_structure__fee_type')
        with transaction.atomic():
            for f in qs.iterator():
                base = max(f.amount - f.discount, Decimal('0.00'))
                rate = f.fee_structure.fee_type.vat_rate_for(f.student.is_saudi)
                expected = (base * (1 + rate)).quantize(Decimal('0.01'))
                if expected == f.net_amount:
                    correct += 1
                    continue
                if not include_paid and f.payments.filter(is_voided=False).exists():
                    skipped_paid += 1
                    self.stdout.write(f'  SKIPPED (has payments) pk={f.pk} {f.student.full_name} '
                                      f'({f.fee_structure.fee_type.name}): {f.net_amount} → {expected}')
                    continue
                self.stdout.write(f'  {"[DRY]" if dry_run else "FIXED"} pk={f.pk} {f.student.full_name} '
                                  f'({f.fee_structure.fee_type.name}): {f.net_amount} → {expected}')
                if not dry_run:
                    f.save()              # recomputes net_amount
                    f.refresh_status()    # PAID may become PARTIAL if the price went up
                fixed += 1

        style = self.style.WARNING if dry_run else self.style.SUCCESS
        self.stdout.write(style(
            f'\nDone. {"Would fix" if dry_run else "Fixed"} {fixed} records, {correct} already correct.'))
        if skipped_paid:
            self.stdout.write(self.style.WARNING(
                f'{skipped_paid} fee(s) with payments were skipped. Re-billing them is a finance '
                'decision — rerun with --include-paid only after approval.'))
