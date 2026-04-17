"""
Management command: seed_grades

Creates all standard grades for every division (American, British, French, Home Study).
Safe to run multiple times (get_or_create).

Usage:
    python manage.py seed_grades
    python manage.py seed_grades --division AMERICAN
"""

from django.core.management.base import BaseCommand
from core.models import Division, Grade


# ── Grade lists by division ──────────────────────────────────────────────────
AMERICAN_GRADES = [
    ('Nursery',    1),
    ('Pre-Kinder', 2),
    ('Kinder 1',   3),
    ('Kinder 2',   4),
    ('Grade 1',    5),
    ('Grade 2',    6),
    ('Grade 3',    7),
    ('Grade 4',    8),
    ('Grade 5',    9),
    ('Grade 6',    10),
    ('Grade 7',    11),
    ('Grade 8',    12),
    ('Grade 9',    13),
    ('Grade 10',   14),
    ('Grade 11',   15),
    ('Grade 12',   16),
]

BRITISH_GRADES = [
    ('Nursery',    1),
    ('Reception',  2),
    ('Year 1',     3),
    ('Year 2',     4),
    ('Year 3',     5),
    ('Year 4',     6),
    ('Year 5',     7),
    ('Year 6',     8),
    ('Year 7',     9),
    ('Year 8',     10),
    ('Year 9',     11),
    ('Year 10',    12),
    ('Year 11',    13),
    ('Year 12',    14),
    ('Year 13',    15),
]

FRENCH_GRADES = [
    ('Nursery',   1),
    ('CP',        2),
    ('CE1',       3),
    ('CE2',       4),
    ('CM1',       5),
    ('CM2',       6),
    ('6ème',      7),
    ('5ème',      8),
    ('4ème',      9),
    ('3ème',      10),
    ('2nde',      11),
    ('1ère',      12),
    ('Terminale', 13),
]

HOME_STUDY_GRADES = [
    ('HS-Foundation', 1),
    ('HS-Primary',    2),
    ('HS-Middle',     3),
    ('HS-Secondary',  4),
]

DIVISION_GRADES = {
    Division.AMERICAN:   AMERICAN_GRADES,
    Division.BRITISH:    BRITISH_GRADES,
    Division.FRENCH:     FRENCH_GRADES,
    Division.HOME_STUDY: HOME_STUDY_GRADES,
}


class Command(BaseCommand):
    help = ('Seed standard grades for all (or a specific) division. '
            'Idempotent — safe to run multiple times.')

    def add_arguments(self, parser):
        parser.add_argument(
            '--division',
            type=str,
            choices=list(DIVISION_GRADES.keys()),
            default=None,
            help='Only seed grades for this division (e.g. AMERICAN). '
                 'Omit to seed all divisions.',
        )

    def handle(self, *args, **options):
        target_div = options.get('division')
        divisions  = Division.objects.filter(is_active=True)

        if target_div:
            divisions = divisions.filter(name=target_div)
            if not divisions.exists():
                self.stderr.write(
                    self.style.ERROR(
                        f"Division '{target_div}' not found or is inactive. "
                        f"Please create it in the admin first."
                    )
                )
                return

        total_created = 0
        total_existing = 0

        for division in divisions:
            grade_list = DIVISION_GRADES.get(division.name, [])
            if not grade_list:
                self.stdout.write(
                    self.style.WARNING(
                        f"No grade template defined for division '{division}'. Skipping."
                    )
                )
                continue

            self.stdout.write(f"\n  Division: {division}")
            created_count = 0
            for name, order in grade_list:
                grade, created = Grade.objects.get_or_create(
                    name=name,
                    division=division,
                    defaults={'order': order},
                )
                if created:
                    created_count   += 1
                    total_created   += 1
                    self.stdout.write(f"    + Created: {grade}")
                else:
                    total_existing  += 1

            self.stdout.write(
                self.style.SUCCESS(
                    f"    → {created_count} created, "
                    f"{len(grade_list) - created_count} already existed."
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nDone. Total created: {total_created}, "
                f"already existed: {total_existing}."
            )
        )
