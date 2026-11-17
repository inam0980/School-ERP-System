"""
fix_student_id_types — repair data affected by BUG-01.

Before the fix, StudentForm never saved `id_type`, so every student created in
the UI was stored as NATIONAL_ID (Saudi → 0 % VAT), even Iqama/Passport holders.

    python manage.py fix_student_id_types            # dry run: report only
    python manage.py fix_student_id_types --apply    # correct id_type

Only `id_type` is changed. Existing fees are NOT re-priced: whether to bill VAT
retroactively is a finance decision (see `recalc_student_fees --dry-run`).
"""
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from fees.models import StudentFee
from students.models import Student


class Command(BaseCommand):
    help = "Correct id_type for non-Saudi students wrongly stored as NATIONAL_ID (dry run by default)."

    def add_arguments(self, parser):
        parser.add_argument('--apply', action='store_true', help='Save the corrections.')

    def handle(self, *args, apply=False, **opts):
        suspects = (Student.objects
                    .filter(id_type=Student.NATIONAL_ID_TYPE)
                    .filter(Q(national_id='') | Q(national_id__isnull=True))
                    .exclude(Q(iqama_number='') & Q(passport_number=''))
                    .order_by('student_id'))

        if not apply:
            self.stdout.write(self.style.WARNING('DRY RUN — nothing will be saved. Use --apply to fix.\n'))

        changed = []
        with transaction.atomic():
            for s in suspects:
                new_type = Student.IQAMA if s.iqama_number.strip() else Student.PASSPORT_ID
                self.stdout.write(f'  {s.student_id}  {s.full_name:<35} NATIONAL_ID -> {new_type}')
                if apply:
                    s.id_type = new_type
                    s.save(update_fields=['id_type', 'updated_at'])
                changed.append(s.pk)

        fees = StudentFee.objects.filter(student_id__in=changed, fee_structure__fee_type__is_taxable=True)
        verb = 'Corrected' if apply else 'Would correct'
        self.stdout.write(self.style.SUCCESS(f'\n{verb} {len(changed)} student(s).'))
        if changed:
            self.stdout.write(
                f'{fees.count()} existing fee(s) on taxable fee types were charged 0 % VAT and were '
                'NOT re-priced. New fees will include VAT. To review re-billing, run:\n'
                '    python manage.py recalc_student_fees --dry-run')
