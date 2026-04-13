"""
management command: seed_initial_data
──────────────────────────────────────
Creates the foundational data required to start using the ERP:

  • 3 Divisions  (American / British / French)
  • 12 Grades per Division (KG1, KG2, Grade 1 … Grade 12)
  • 1 Section "A" per Grade
  • Current Academic Year  (e.g. 2024-25)
  • Default SUPER_ADMIN user  (admin / admin@school.sa / AdminPass123!)

Run once after first deployment:
    python manage.py seed_initial_data

Options:
    --year      Academic year label            default: "2024-25"
    --admin-username   Superuser username      default: admin
    --admin-email      Superuser email         default: admin@school.sa
    --admin-password   Superuser password      default: AdminPass123!
    --no-input  Skip all confirmation prompts
"""

import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


class Command(BaseCommand):
    help = "Seed initial data: divisions, grades, sections, academic year, and admin user"

    def add_arguments(self, parser):
        parser.add_argument(
            '--year', default='2024-25',
            help='Academic year label, e.g. 2024-25',
        )
        parser.add_argument(
            '--admin-username', default='admin',
            dest='admin_username',
        )
        parser.add_argument(
            '--admin-email', default='admin@school.sa',
            dest='admin_email',
        )
        parser.add_argument(
            '--admin-password', default='AdminPass123!',
            dest='admin_password',
        )
        parser.add_argument(
            '--no-input', action='store_true', dest='no_input',
            help='Skip confirmation prompts',
        )

    def handle(self, *args, **options):
        if not options['no_input']:
            self.stdout.write(
                self.style.WARNING(
                    "\nThis command will create divisions, grades, sections, an academic year,\n"
                    "and a default super-admin user.  Existing records are NOT overwritten.\n"
                )
            )
            confirm = input("Continue? [y/N] ").strip().lower()
            if confirm != 'y':
                self.stdout.write("Aborted.")
                return

        with transaction.atomic():
            self._create_divisions_and_grades()
            self._create_academic_year(options['year'])
            self._create_admin(
                options['admin_username'],
                options['admin_email'],
                options['admin_password'],
            )

        self.stdout.write(self.style.SUCCESS("\n✓ Initial data seeded successfully."))
        self.stdout.write(
            f"  Login: {options['admin_username']} / {options['admin_password']}\n"
            "  Change the password immediately after first login!"
        )

    # ─────────────────────────────────────────────────────────────────────────

    def _create_divisions_and_grades(self):
        from core.models import Division, Grade, Section

        DIVISIONS = [
            (Division.AMERICAN, Division.AMERICAN),
            (Division.BRITISH,  Division.BRITISH),
            (Division.FRENCH,   Division.FRENCH),
        ]

        GRADES = [
            ('KG1',      0),
            ('KG2',      1),
            ('Grade 1',  2),
            ('Grade 2',  3),
            ('Grade 3',  4),
            ('Grade 4',  5),
            ('Grade 5',  6),
            ('Grade 6',  7),
            ('Grade 7',  8),
            ('Grade 8',  9),
            ('Grade 9',  10),
            ('Grade 10', 11),
            ('Grade 11', 12),
            ('Grade 12', 13),
        ]

        for (div_name, curriculum) in DIVISIONS:
            division, created = Division.objects.get_or_create(
                name=div_name,
                defaults={'curriculum_type': curriculum},
            )
            if created:
                self.stdout.write(f"  Created division: {division}")
            else:
                self.stdout.write(f"  Division exists:  {division}")

            for (grade_name, order) in GRADES:
                grade, g_created = Grade.objects.get_or_create(
                    name=grade_name,
                    division=division,
                    defaults={'order': order},
                )
                if g_created:
                    self.stdout.write(f"    + Grade {grade_name}")

                # Create one default section "A"
                section, s_created = Section.objects.get_or_create(
                    name='A',
                    grade=grade,
                )
                if s_created:
                    self.stdout.write(f"      + Section A")

    def _create_academic_year(self, label: str):
        from core.models import AcademicYear

        # Parse "2024-25" → start 2024-09-01, end 2025-06-30
        try:
            start_y = int(label.split('-')[0])
            end_y   = start_y + 1
        except (ValueError, IndexError):
            raise CommandError(f"Invalid year format '{label}'. Use e.g. '2024-25'.")

        year, created = AcademicYear.objects.get_or_create(
            name=label,
            defaults={
                'start_date': datetime.date(start_y, 9, 1),
                'end_date':   datetime.date(end_y, 6, 30),
                'is_current': True,
            },
        )
        if created:
            self.stdout.write(f"  Created academic year: {year}")
        else:
            self.stdout.write(f"  Academic year exists:  {year}")

    def _create_admin(self, username: str, email: str, password: str):
        from accounts.models import CustomUser

        if CustomUser.objects.filter(username=username).exists():
            self.stdout.write(f"  Admin user '{username}' already exists — skipped.")
            return

        user = CustomUser.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            full_name='System Administrator',
            role=CustomUser.SUPER_ADMIN,
        )
        self.stdout.write(f"  Created super-admin: {user.username} <{user.email}>")
