"""
management command: seed_demo_data
────────────────────────────────────────────────────────────────────
Populates the database with realistic demo records so the ERP is
immediately explorable without manual data entry.

Creates:
  • Staff users  (teachers, accountant, receptionist)
  • Subjects     for Grade 5 American and Grade 7 British
  • 40 Students  (mix of Saudi / non-Saudi with realistic names)
  • Attendance   for the last 30 school days
  • Exam types, Exams, Marks
  • Fee types, Fee structures, Student fees, Payments

Run:
    python manage.py seed_demo_data
    python manage.py seed_demo_data --no-input   # skip confirmation
"""

import datetime
import random
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction


# ─────────────────────────────────────────────────────────────────
#  Data pools
# ─────────────────────────────────────────────────────────────────

SAUDI_STUDENTS = [
    ("Mohammed Al-Zahrani",    "محمد الزهراني",    "M", "Saudi",   "NATIONAL_ID", "1098765432"),
    ("Abdullah Al-Qahtani",    "عبدالله القحطاني", "M", "Saudi",   "NATIONAL_ID", "1087654321"),
    ("Omar Al-Shehri",         "عمر الشهري",       "M", "Saudi",   "NATIONAL_ID", "1076543219"),
    ("Yazeed Al-Ghamdi",       "يزيد الغامدي",     "M", "Saudi",   "NATIONAL_ID", "1065432198"),
    ("Faisal Al-Maliki",       "فيصل المالكي",     "M", "Saudi",   "NATIONAL_ID", "1054321987"),
    ("Turki Al-Dosari",        "تركي الدوسري",     "M", "Saudi",   "NATIONAL_ID", "1043219876"),
    ("Salman Al-Harbi",        "سلمان الحربي",     "M", "Saudi",   "NATIONAL_ID", "1032198765"),
    ("Khalid Al-Otaibi",       "خالد العتيبي",     "M", "Saudi",   "NATIONAL_ID", "1021987654"),
    ("Noura Al-Sulami",        "نورة السلمي",      "F", "Saudi",   "NATIONAL_ID", "2098765432"),
    ("Reema Al-Rashid",        "ريما الراشد",      "F", "Saudi",   "NATIONAL_ID", "2087654321"),
    ("Sara Al-Anazi",          "سارة العنزي",      "F", "Saudi",   "NATIONAL_ID", "2076543219"),
    ("Dalal Al-Mutairi",       "دلال المطيري",     "F", "Saudi",   "NATIONAL_ID", "2065432198"),
    ("Hessa Al-Dossari",       "حصة الدوسري",      "F", "Saudi",   "NATIONAL_ID", "2054321987"),
    ("Lujain Al-Saud",         "لجين آل سعود",     "F", "Saudi",   "NATIONAL_ID", "2043219876"),
    ("Dana Al-Fayez",          "دانا الفايز",      "F", "Saudi",   "NATIONAL_ID", "2032198765"),
    ("Raghad Al-Zahrani",      "رغد الزهراني",     "F", "Saudi",   "NATIONAL_ID", "2021987654"),
]

EXPAT_STUDENTS = [
    ("Ahmed Hassan",           "أحمد حسن",         "M", "Egyptian",  "IQAMA", "2198765432"),
    ("Omar Farouq",            "عمر فاروق",         "M", "Egyptian",  "IQAMA", "2187654321"),
    ("Ali Al-Yemeni",          "علي اليمني",        "M", "Yemeni",    "IQAMA", "2176543219"),
    ("Hassan Al-Sudani",       "حسن السوداني",      "M", "Sudanese",  "IQAMA", "2165432198"),
    ("Bilal Chaudhry",         "بلال چودھری",       "M", "Pakistani", "IQAMA", "2154321987"),
    ("Imran Khan Jr",          "عمران خان",          "M", "Pakistani", "IQAMA", "2143219876"),
    ("Rahul Sharma",           "راهول شارما",        "M", "Indian",    "IQAMA", "2132198765"),
    ("Arjun Patel",            "ارجون باتيل",        "M", "Indian",    "IQAMA", "2121987654"),
    ("James Okafor",           "جيمس أوكافور",       "M", "Nigerian",  "PASSPORT", "A12345678"),
    ("Lucas Fernandez",        "لوكاس فيرنانديز",    "M", "Spanish",   "PASSPORT", "XBA123456"),
    ("Fatima Al-Iraqi",        "فاطمة العراقي",      "F", "Iraqi",     "IQAMA", "2298765432"),
    ("Mariam Al-Libi",         "مريم الليبي",        "F", "Libyan",    "IQAMA", "2287654321"),
    ("Zara Ahmed",             "زارا أحمد",          "F", "Pakistani", "IQAMA", "2276543219"),
    ("Priya Nair",             "بريا ناير",          "F", "Indian",    "IQAMA", "2265432198"),
    ("Sofia Russo",            "صوفيا روسو",         "F", "Italian",   "PASSPORT", "AB1234567"),
    ("Emma Wilson",            "إيما ويلسون",        "F", "British",   "PASSPORT", "GB9876543"),
    ("Amira Benali",           "أميرة بنعلي",        "F", "Algerian",  "IQAMA", "2243219876"),
    ("Nadia Khalil",           "نادية خليل",         "F", "Lebanese",  "IQAMA", "2232198765"),
    ("Aisha Diallo",           "عائشة ديالو",        "F", "Senegalese","PASSPORT", "SN1234560"),
    ("Lin Wei",                "لين وي",             "F", "Chinese",   "PASSPORT", "E98765432"),
    ("Sana Mirza",             "سنا ميرزا",          "F", "Pakistani", "IQAMA", "2210987654"),
    ("Rania El-Sawi",          "رانيا السوي",        "F", "Egyptian",  "IQAMA", "2209876543"),
    ("Amara Traoré",           "أمارا تراوري",       "M", "Malian",    "PASSPORT", "ML9876543"),
    ("Ryan O'Brien",           "رايان أوبراين",      "M", "Irish",     "PASSPORT", "IE1234567"),
]

STAFF_USERS = [
    ("teacher1",  "teacher1@school.sa",  "Sara Al-Khalidi",     "TEACHER",     "TeacherPass1!"),
    ("teacher2",  "teacher2@school.sa",  "Mohammed Al-Rashidi", "TEACHER",     "TeacherPass2!"),
    ("teacher3",  "teacher3@school.sa",  "Priya Subramaniam",   "TEACHER",     "TeacherPass3!"),
    ("accountant","accountant@school.sa","Khalid Al-Amri",      "ACCOUNTANT",  "AccountPass1!"),
    ("reception", "reception@school.sa", "Hind Al-Maliki",      "STAFF",       "StaffPass1!"),
]

SUBJECTS_G5_AM = [
    ("Mathematics",        "MATH-G5-AM"),
    ("English Language",   "ENG-G5-AM"),
    ("Science",            "SCI-G5-AM"),
    ("Social Studies",     "SS-G5-AM"),
    ("Arabic Language",    "ARB-G5-AM"),
    ("Islamic Studies",    "ISL-G5-AM"),
    ("Physical Education", "PE-G5-AM"),
    ("Art",                "ART-G5-AM"),
]

SUBJECTS_G7_BR = [
    ("Mathematics",        "MATH-G7-BR"),
    ("English Language",   "ENG-G7-BR"),
    ("Biology",            "BIO-G7-BR"),
    ("Physics",            "PHY-G7-BR"),
    ("Chemistry",          "CHEM-G7-BR"),
    ("Arabic Language",    "ARB-G7-BR"),
    ("Islamic Studies",    "ISL-G7-BR"),
    ("History",            "HIST-G7-BR"),
]

FEE_TYPES = [
    ("Tuition Fee",      "TUITION",         False, Decimal("28000.00")),
    ("Transport Fee",    "TRANSPORT",        False, Decimal("4800.00")),
    ("Uniform Fee",      "UNIFORM",          True,  Decimal("950.00")),
    ("Books & Supplies", "BOOKS",            True,  Decimal("1200.00")),
    ("Activity Fee",     "EXTRACURRICULAR",  False, Decimal("600.00")),
]


class Command(BaseCommand):
    help = "Seed realistic demo data for exploring the ERP"

    def add_arguments(self, parser):
        parser.add_argument('--no-input', action='store_true', dest='no_input')

    def handle(self, *args, **options):
        if not options['no_input']:
            self.stdout.write(self.style.WARNING(
                "\nThis will add demo students, staff, attendance, marks and fees.\n"
                "Existing records are NOT deleted — run once on a fresh DB.\n"
            ))
            if input("Continue? [y/N] ").strip().lower() != 'y':
                self.stdout.write("Aborted.")
                return

        with transaction.atomic():
            admin       = self._get_admin()
            year        = self._get_current_year()
            am_div, br_div = self._get_divisions()
            g5_am, sec_g5  = self._get_grade_section("Grade 5", am_div)
            g7_br, sec_g7  = self._get_grade_section("Grade 7", br_div)

            staff       = self._create_staff()
            teacher     = staff[0]   # first teacher marks attendance/exams

            subjs_g5    = self._create_subjects(SUBJECTS_G5_AM, g5_am, am_div)
            subjs_g7    = self._create_subjects(SUBJECTS_G7_BR, g7_br, br_div)

            students_g5 = self._create_students(SAUDI_STUDENTS[:8] + EXPAT_STUDENTS[:8],
                                                 am_div, g5_am, sec_g5, year, admin)
            students_g7 = self._create_students(SAUDI_STUDENTS[8:] + EXPAT_STUDENTS[8:],
                                                 br_div, g7_br, sec_g7, year, admin)

            all_students = students_g5 + students_g7

            self._create_attendance(all_students, teacher)
            self._create_exams_and_marks(subjs_g5, sec_g5, year, students_g5, teacher)
            self._create_exams_and_marks(subjs_g7, sec_g7, year, students_g7, teacher)
            fee_types   = self._create_fee_types()
            self._create_fees(fee_types, g5_am, am_div, year, students_g5, admin)
            self._create_fees(fee_types, g7_br, br_div, year, students_g7, admin)

        self.stdout.write(self.style.SUCCESS(
            f"\n✓ Demo data seeded.\n"
            f"  {len(all_students)} students   "
            f"  {len(staff)} staff users\n"
            f"  Logins: teacher1/TeacherPass1!  accountant/AccountPass1!\n"
        ))

    # ─────────────────────────────────────────────────────────────

    def _get_admin(self):
        from accounts.models import CustomUser
        admin = CustomUser.objects.filter(role='SUPER_ADMIN').first()
        if not admin:
            admin = CustomUser.objects.filter(is_superuser=True).first()
        if not admin:
            self.stdout.write(self.style.ERROR(
                "No admin user found. Run seed_initial_data first."
            ))
            raise SystemExit(1)
        return admin

    def _get_current_year(self):
        from core.models import AcademicYear
        year = AcademicYear.objects.filter(is_current=True).first()
        if not year:
            self.stdout.write(self.style.ERROR(
                "No current academic year found. Run seed_initial_data first."
            ))
            raise SystemExit(1)
        self.stdout.write(f"  Using year: {year}")
        return year

    def _get_divisions(self):
        from core.models import Division
        am = Division.objects.filter(name='AMERICAN').first()
        br = Division.objects.filter(name='BRITISH').first()
        if not am or not br:
            self.stdout.write(self.style.ERROR(
                "American/British divisions missing. Run seed_initial_data first."
            ))
            raise SystemExit(1)
        return am, br

    def _get_grade_section(self, grade_name, division):
        from core.models import Grade, Section
        grade = Grade.objects.filter(name=grade_name, division=division).first()
        if not grade:
            self.stdout.write(self.style.ERROR(
                f"Grade '{grade_name}' not found for {division}. Run seed_initial_data first."
            ))
            raise SystemExit(1)
        # Ensure section B exists (seed creates only A)
        section_a = Section.objects.get_or_create(name='A', grade=grade)[0]
        section_b, _ = Section.objects.get_or_create(name='B', grade=grade)
        self.stdout.write(f"  Grade: {grade}  Sections: A, B")
        return grade, section_a

    def _create_staff(self):
        from accounts.models import CustomUser
        created = []
        for username, email, full_name, role, password in STAFF_USERS:
            user, new = CustomUser.objects.get_or_create(
                username=username,
                defaults={'email': email, 'full_name': full_name, 'role': role, 'is_active': True},
            )
            if new:
                user.set_password(password)
                user.save()
                self.stdout.write(f"  + Staff: {username} ({role})")
            created.append(user)
        return created

    def _create_subjects(self, subject_list, grade, division):
        from core.models import Subject
        subjects = []
        for name, code in subject_list:
            subj, created = Subject.objects.get_or_create(
                code=code,
                defaults={'name': name, 'grade': grade, 'division': division},
            )
            if created:
                self.stdout.write(f"  + Subject: {code}")
            subjects.append(subj)
        return subjects

    def _create_students(self, data_rows, division, grade, section, year, admin):
        from students.models import Student
        import datetime

        created = []
        dobs = [
            datetime.date(2012, 3, 15), datetime.date(2012, 7, 22),
            datetime.date(2013, 1, 10), datetime.date(2013, 5, 8),
            datetime.date(2012, 11, 30), datetime.date(2013, 9, 19),
            datetime.date(2012, 4, 25), datetime.date(2013, 2, 14),
            datetime.date(2011, 6, 5),  datetime.date(2011, 8, 17),
            datetime.date(2010, 12, 3), datetime.date(2010, 3, 28),
            datetime.date(2011, 10, 11), datetime.date(2011, 1, 7),
            datetime.date(2010, 7, 19), datetime.date(2010, 9, 23),
        ]

        for i, row in enumerate(data_rows):
            full_name, arabic_name, gender, nationality, id_type, national_id = row
            if Student.objects.filter(full_name=full_name, academic_year=year).exists():
                s = Student.objects.get(full_name=full_name, academic_year=year)
                created.append(s)
                continue

            dob = dobs[i % len(dobs)]
            s = Student.objects.create(
                full_name=full_name,
                arabic_name=arabic_name,
                dob=dob,
                gender=gender,
                nationality=nationality,
                id_type=id_type,
                national_id=national_id,
                division=division,
                grade=grade,
                section=section,
                academic_year=year,
                roll_number=str(i + 1).zfill(2),
                father_name=f"{full_name.split()[0]} Al-{full_name.split()[-1]}",
                arabic_father=f"أبو {arabic_name.split()[0]}",
                guardian_phone=f"05{random.randint(10000000, 99999999)}",
                guardian_phone2=f"05{random.randint(10000000, 99999999)}",
                guardian_email=f"{full_name.split()[0].lower()}.guardian@gmail.com",
                address=f"{random.randint(1,200)} Al-Nuzha Street, Jeddah",
                arabic_address=f"شارع النزهة، رقم {random.randint(1,200)}، جدة",
                enrollment_type='NEW',
                admission_date=year.start_date,
                is_active=True,
                created_by=admin,
            )
            created.append(s)
            self.stdout.write(f"  + Student: {full_name}")
        return created

    def _create_attendance(self, students, teacher):
        from attendance.models import Attendance
        import datetime

        today  = datetime.date.today()
        # generate last 30 weekdays
        school_days = []
        d = today
        while len(school_days) < 30:
            if d.weekday() < 5:   # Mon–Fri (adjust for Sun–Thu if needed)
                school_days.append(d)
            d -= datetime.timedelta(days=1)

        # weights: mostly present
        statuses  = ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'A', 'L', 'E']
        count = 0
        for student in students:
            for day in school_days:
                if not Attendance.objects.filter(student=student, date=day).exists():
                    Attendance.objects.create(
                        student=student,
                        date=day,
                        status=random.choice(statuses),
                        marked_by=teacher,
                    )
                    count += 1
        self.stdout.write(f"  + Attendance records: {count}")

    def _create_exams_and_marks(self, subjects, section, year, students, teacher):
        from academics.models import ExamType, Exam, Mark

        exam_types_data = [
            ("Quiz",    20),
            ("MidTerm", 40),
            ("Final",   40),
        ]
        exam_types = {}
        for name, weight in exam_types_data:
            et, _ = ExamType.objects.get_or_create(name=name, defaults={'weight_percentage': weight})
            exam_types[name] = et

        terms = ['T1', 'T2']
        exam_count = 0
        mark_count = 0

        for term in terms:
            base_date = year.start_date + datetime.timedelta(days=30 if term == 'T1' else 120)
            for et_name, et in exam_types.items():
                for subj in subjects[:4]:   # first 4 subjects per section to keep count manageable
                    exam_name = f"{et_name} — {subj.name} ({term})"
                    exam, created = Exam.objects.get_or_create(
                        name=exam_name,
                        subject=subj,
                        section=section,
                        academic_year=year,
                        defaults={
                            'exam_type': et,
                            'term': term,
                            'date': base_date,
                            'total_marks': 100,
                            'created_by': teacher,
                        },
                    )
                    if created:
                        exam_count += 1
                    for student in students:
                        if not Mark.objects.filter(student=student, exam=exam).exists():
                            absent = random.random() < 0.04   # 4% absent
                            Mark.objects.create(
                                student=student,
                                exam=exam,
                                is_absent=absent,
                                obtained_marks=None if absent else Decimal(str(random.randint(55, 100))),
                                status='submitted',
                                entered_by=teacher,
                            )
                            mark_count += 1
                    base_date += datetime.timedelta(days=3)

        self.stdout.write(f"  + Exams: {exam_count}   Marks: {mark_count}")

    def _create_fee_types(self):
        from fees.models import FeeType
        created = []
        for name, category, taxable, _ in FEE_TYPES:
            ft, new = FeeType.objects.get_or_create(
                name=name,
                defaults={'category': category, 'is_taxable': taxable},
            )
            if new:
                self.stdout.write(f"  + FeeType: {name}")
            created.append((ft, _))
        return created

    def _create_fees(self, fee_types, grade, division, year, students, admin):
        from fees.models import FeeStructure, StudentFee, Payment

        due = year.start_date + datetime.timedelta(days=30)

        for ft, amount in fee_types:
            structure, _ = FeeStructure.objects.get_or_create(
                academic_year=year,
                grade=grade,
                division=division,
                fee_type=ft,
                defaults={
                    'amount': amount,
                    'due_date': due,
                    'frequency': 'ANNUAL',
                },
            )

            for student in students:
                if StudentFee.objects.filter(student=student, fee_structure=structure).exists():
                    continue

                discount     = Decimal('0.00')
                discount_note = ''
                # 10% sibling discount for every 3rd student
                if students.index(student) % 3 == 2:
                    discount = (amount * Decimal('0.10')).quantize(Decimal('0.01'))
                    discount_note = 'Sibling discount 10%'

                tax = (amount * Decimal('0.15')).quantize(Decimal('0.01')) if ft.is_taxable else Decimal('0.00')
                net = amount - discount + tax

                # Randomly assign payment status
                roll = random.random()
                if roll < 0.40:
                    status = 'PAID'
                elif roll < 0.55:
                    status = 'PARTIAL'
                elif roll < 0.70:
                    status = 'UNPAID'
                else:
                    status = 'OVERDUE'

                sf = StudentFee.objects.create(
                    student=student,
                    fee_structure=structure,
                    amount=amount,
                    discount=discount,
                    discount_note=discount_note,
                    net_amount=net,
                    due_date=due,
                    status=status,
                    assigned_by=admin,
                )

                # Add a payment for PAID and PARTIAL
                if status in ('PAID', 'PARTIAL'):
                    paid_amt = net if status == 'PAID' else (net * Decimal('0.50')).quantize(Decimal('0.01'))
                    Payment.objects.create(
                        student_fee=sf,
                        paid_amount=paid_amt,
                        payment_date=year.start_date + datetime.timedelta(days=random.randint(5, 60)),
                        payment_method=random.choice(['CASH', 'BANK', 'MADA']),
                        collected_by=admin,
                        notes='Demo payment',
                    )

        self.stdout.write(f"  + Fees & payments assigned for {len(students)} students")
