"""
python manage.py seed_students [--yes]

Wipes ALL existing academic + student data, then seeds:
  • 1 AcademicYear  (2025-26, current)
  • 4 Divisions     (American, British, French, Home Study)
  • 17 Grades       (Nursery → Grade 12) per division  = 68 grades
  • 3 Sections      (A, B, C)            per grade     = 204 sections
  • 5 Students                           per section   = 1 020 students
"""

import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models     import AcademicYear, Division, Grade, Section
from students.models import Student
from fees.models import (
    PaymentPlanInstallment, PaymentPlan, Payment, TaxInvoice,
    StudentFee, BundleInstallment, FeeStructureBundle, FeeStructure,
    TuitionInstallment, TuitionFeeConfig, Salary, FeeType,
)
from academics.models import Mark, Exam, ReportCard, GradeConfig, ExamType
from attendance.models import Attendance, StaffAttendance

# ── Name pools ────────────────────────────────────────────────────────
MALE_FIRST = [
    "Ahmed", "Mohammed", "Abdullah", "Omar", "Ali", "Hassan", "Ibrahim",
    "Khalid", "Faisal", "Yusuf", "Tariq", "Saad", "Nasser", "Rayan",
    "Adam", "Bilal", "Hamza", "Ziad", "Waleed", "Sami",
]
FEMALE_FIRST = [
    "Fatima", "Aisha", "Mariam", "Sara", "Nour", "Hana", "Lina",
    "Reem", "Dana", "Layla", "Hessa", "Shahd", "Noura", "Maha",
    "Rana", "Dina", "Sana", "Rima", "Lujain", "Arwa",
]
LAST_NAMES = [
    "Al-Rashid", "Al-Qahtani", "Al-Ghamdi", "Al-Harbi", "Al-Otaibi",
    "Al-Zahrani", "Al-Shehri", "Al-Dossari", "Al-Mutairi", "Al-Ahmadi",
    "Al-Anazi", "Al-Jaber", "Al-Maliki", "Al-Subaie", "Al-Shahrani",
]
ARABIC_MALE   = ["أحمد", "محمد", "عبدالله", "عمر", "علي", "حسن", "إبراهيم", "خالد", "فيصل", "يوسف"]
ARABIC_FEMALE = ["فاطمة", "عائشة", "مريم", "سارة", "نور", "هناء", "لينا", "ريم", "دانا", "ليلى"]
ARABIC_LAST   = ["الراشد", "القحطاني", "الغامدي", "الحربي", "العتيبي", "الزهراني"]
NATIONALITIES_OTHER = [
    "Egyptian", "Pakistani", "Indian", "Jordanian",
    "Yemeni", "Sudanese", "Lebanese",
]

GRADE_NAMES = [
    ("Nursery",     0),
    ("Pre-Kinder",  1),
    ("Kinder 1",    2),
    ("Kinder 2",    3),
    ("Reception",   4),
    ("Grade 1",     5),
    ("Grade 2",     6),
    ("Grade 3",     7),
    ("Grade 4",     8),
    ("Grade 5",     9),
    ("Grade 6",    10),
    ("Grade 7",    11),
    ("Grade 8",    12),
    ("Grade 9",    13),
    ("Grade 10",   14),
    ("Grade 11",   15),
    ("Grade 12",   16),
]

SECTIONS     = ["A", "B", "C"]
STUDENTS_PER = 5


def _dob_for_grade(order: int) -> date:
    base_age = 3 + order
    noise    = random.randint(-6, 6)
    return date(2026, 1, 1) - timedelta(days=base_age * 365 + noise * 30)


def _phone() -> str:
    return f"05{random.randint(10000000, 99999999)}"


def _nid() -> str:
    return str(random.randint(1000000000, 9999999999))


class Command(BaseCommand):
    help = "Wipe all data and seed fresh students, grades, and sections"

    def add_arguments(self, parser):
        parser.add_argument("--yes", action="store_true",
                            help="Skip confirmation prompt")

    @transaction.atomic
    def handle(self, *args, **options):
        if not options["yes"]:
            ans = input(
                "\n⚠️  ALL existing data will be DELETED (students, fees, marks, "
                "attendance, grades, sections, divisions, academic years).\n"
                "Type YES to continue: "
            ).strip()
            if ans != "YES":
                self.stdout.write(self.style.WARNING("Aborted."))
                return

        # ── 1. Wipe in correct dependency order (children before parents) ──
        self.stdout.write("Deleting all existing data …")
        # Fees (deepest first)
        PaymentPlanInstallment.objects.all().delete()
        PaymentPlan.objects.all().delete()
        Payment.objects.all().delete()
        TaxInvoice.objects.all().delete()
        StudentFee.objects.all().delete()
        BundleInstallment.objects.all().delete()
        FeeStructureBundle.objects.all().delete()
        FeeStructure.objects.all().delete()
        TuitionInstallment.objects.all().delete()
        TuitionFeeConfig.objects.all().delete()
        Salary.objects.all().delete()
        FeeType.objects.all().delete()
        # Academics
        Mark.objects.all().delete()
        Exam.objects.all().delete()
        ReportCard.objects.all().delete()
        GradeConfig.objects.all().delete()
        ExamType.objects.all().delete()
        # Attendance
        StaffAttendance.objects.all().delete()
        Attendance.objects.all().delete()
        # Fee types (safe to delete now — FeeStructure already gone)
        FeeType.objects.all().delete()
        # Students / core
        Student.objects.all().delete()
        Section.objects.all().delete()
        Grade.objects.all().delete()
        Division.objects.all().delete()
        AcademicYear.objects.all().delete()
        self.stdout.write("  ✔ All old data cleared.")

        # ── 2. Academic Year ──────────────────────────────────────────
        year = AcademicYear.objects.create(
            name       = "2025-26",
            start_date = date(2025, 9, 1),
            end_date   = date(2026, 6, 30),
            is_current = True,
        )
        self.stdout.write(f"  ✔ Academic Year: {year}")

        # ── 3. Divisions ──────────────────────────────────────────────
        divisions_data = [
            (Division.AMERICAN,   Division.AMERICAN),
            (Division.BRITISH,    Division.BRITISH),
            (Division.FRENCH,     Division.FRENCH),
            (Division.HOME_STUDY, Division.HOME_STUDY),
        ]
        divisions = []
        for dname, curriculum in divisions_data:
            d = Division.objects.create(
                name=dname, curriculum_type=curriculum, is_active=True
            )
            divisions.append(d)
            self.stdout.write(f"  ✔ Division: {d}")

        # ── 4. Fee Types ──────────────────────────────────────────────
        fee_types_data = [
            # (name,                      category,                    is_taxable)
            ("Tuition Fee",               FeeType.TUITION,             True),
            ("Admission Fee",             FeeType.ADMISSION,           False),
            ("Registration Fee",          FeeType.REGISTRATION,        False),
            ("Examination Fee",           FeeType.EXAMINATION,         True),
            ("Transport Fee",             FeeType.TRANSPORT,           True),
            ("Uniform Fee",               FeeType.UNIFORM,             True),
            ("Books & Supplies",          FeeType.BOOKS,               True),
            ("Extracurricular Activities",FeeType.EXTRACURRICULAR,     True),
            ("Library Fee",               FeeType.LIBRARY,             True),
            ("Laboratory Fee",            FeeType.LABORATORY,          True),
            ("Sports Fee",               FeeType.SPORTS,              True),
            ("Development Fee",           FeeType.DEVELOPMENT,         False),
            ("Smart Class / IT Fee",      FeeType.SMART_CLASS,         True),
            ("ID Card Fee",               FeeType.ID_CARD,             True),
            ("Security Deposit",          FeeType.SECURITY_DEPOSIT,    False),
            ("Late Fee / Fine",           FeeType.LATE_FEE,            True),
        ]
        for fname, fcat, taxable in fee_types_data:
            FeeType.objects.create(name=fname, category=fcat, is_taxable=taxable)
        self.stdout.write(f"  ✔ Created {len(fee_types_data)} fee types")

        # ── 5. Grades + Sections + Students ──────────────────────────
        total_students = 0
        student_seq    = 1          # global counter → unique student_id per run
        for division in divisions:
            div_code = division.name[:2].upper()   # AM / BR / FR / HO
            for grade_name, order in GRADE_NAMES:
                grade = Grade.objects.create(
                    name=grade_name, division=division, order=order
                )
                for sec_name in SECTIONS:
                    section = Section.objects.create(name=sec_name, grade=grade)

                    for i in range(1, STUDENTS_PER + 1):
                        is_male = (i % 2 == 1)
                        if is_male:
                            first = random.choice(MALE_FIRST)
                            ar_f  = random.choice(ARABIC_MALE)
                        else:
                            first = random.choice(FEMALE_FIRST)
                            ar_f  = random.choice(ARABIC_FEMALE)

                        last    = random.choice(LAST_NAMES)
                        ar_last = random.choice(ARABIC_LAST)

                        is_saudi = random.random() < 0.6
                        if is_saudi:
                            nationality = "Saudi"
                            id_type     = Student.NATIONAL_ID_TYPE
                        else:
                            nationality = random.choice(NATIONALITIES_OTHER)
                            id_type     = random.choice(
                                [Student.IQAMA, Student.PASSPORT_ID]
                            )

                        Student.objects.create(
                            student_id      = f"AKS-2025-{div_code}-{student_seq:05d}",
                            full_name       = f"{first} {last}",
                            arabic_name     = f"{ar_f} {ar_last}",
                            dob             = _dob_for_grade(order),
                            gender          = Student.MALE if is_male else Student.FEMALE,
                            nationality     = nationality,
                            id_type         = id_type,
                            national_id     = _nid(),
                            division        = division,
                            grade           = grade,
                            section         = section,
                            academic_year   = year,
                            roll_number     = str(i).zfill(2),
                            father_name     = f"Mr. {random.choice(MALE_FIRST)} {last}",
                            arabic_father   = f"{random.choice(ARABIC_MALE)} {ar_last}",
                            mother_name     = f"Mrs. {random.choice(FEMALE_FIRST)} {last}",
                            arabic_mother   = f"{random.choice(ARABIC_FEMALE)} {ar_last}",
                            guardian_phone  = _phone(),
                            guardian_email  = (
                                f"{first.lower()}"
                                f".{last.lower().replace('-', '')}"
                                "@example.com"
                            ),
                            enrollment_type = Student.NEW,
                            admission_date  = date(2025, 9, 1),
                            is_active       = True,
                        )
                        total_students += 1
                        student_seq    += 1

        self.stdout.write(self.style.SUCCESS(
            f"\n✅  Seeding complete!\n"
            f"    Divisions : {len(divisions)}\n"
            f"    Fee Types : {len(fee_types_data)}\n"
            f"    Grades    : {len(GRADE_NAMES) * len(divisions)}\n"
            f"    Sections  : {len(GRADE_NAMES) * len(divisions) * len(SECTIONS)}\n"
            f"    Students  : {total_students}\n"
        ))
