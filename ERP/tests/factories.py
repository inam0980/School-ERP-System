"""
Shared factory-boy factories for all tests.
Each factory creates a minimal valid object with sensible defaults.
"""
import datetime
from decimal import Decimal
import factory
from factory.django import DjangoModelFactory

from accounts.models import CustomUser
from core.models import AcademicYear, Division, Grade, Section, Subject
from students.models import Student
from attendance.models import Attendance
from academics.models import ExamType, Exam, Mark
from fees.models import FeeType, FeeStructure, StudentFee, Payment


# ── Accounts ──────────────────────────────────────────────────────────────────

class UserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    username  = factory.Sequence(lambda n: f"user{n}")
    email     = factory.Sequence(lambda n: f"user{n}@school.sa")
    full_name = factory.Sequence(lambda n: f"Test User {n}")
    role      = CustomUser.ADMIN
    is_active = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        password = kwargs.pop("password", "TestPass123!")
        obj = model_class(*args, **kwargs)
        obj.set_password(password)
        obj.save()
        return obj


class TeacherFactory(UserFactory):
    role = CustomUser.TEACHER


class AccountantFactory(UserFactory):
    role = CustomUser.ACCOUNTANT


# ── Core ──────────────────────────────────────────────────────────────────────

class AcademicYearFactory(DjangoModelFactory):
    class Meta:
        model = AcademicYear
        django_get_or_create = ('name',)

    name       = "2024-25"
    start_date = datetime.date(2024, 9, 1)
    end_date   = datetime.date(2025, 6, 30)
    is_current = True


class DivisionFactory(DjangoModelFactory):
    class Meta:
        model = Division
        django_get_or_create = ('name',)

    name            = Division.AMERICAN
    curriculum_type = Division.AMERICAN


class GradeFactory(DjangoModelFactory):
    class Meta:
        model = Grade

    name     = factory.Sequence(lambda n: f"Grade {n+1}")
    division = factory.SubFactory(DivisionFactory)
    order    = factory.Sequence(lambda n: n)


class SectionFactory(DjangoModelFactory):
    class Meta:
        model = Section

    name  = factory.Sequence(lambda n: chr(65 + n % 26))   # A, B, C …
    grade = factory.SubFactory(GradeFactory)


class SubjectFactory(DjangoModelFactory):
    class Meta:
        model = Subject

    name     = factory.Sequence(lambda n: f"Subject {n}")
    code     = factory.Sequence(lambda n: f"SUB-{n:04d}")
    grade    = factory.SubFactory(GradeFactory)
    division = factory.SubFactory(DivisionFactory)


# ── Students ──────────────────────────────────────────────────────────────────

class StudentFactory(DjangoModelFactory):
    class Meta:
        model = Student

    full_name      = factory.Sequence(lambda n: f"Student {n}")
    arabic_name    = factory.Sequence(lambda n: f"طالب {n}")
    dob            = datetime.date(2010, 1, 1)
    gender         = Student.MALE
    nationality    = "Saudi"
    national_id    = factory.Sequence(lambda n: f"100000{n:04d}")
    division       = factory.SubFactory(DivisionFactory)
    grade          = factory.SubFactory(GradeFactory)
    section        = factory.SubFactory(SectionFactory)
    academic_year  = factory.SubFactory(AcademicYearFactory)
    admission_date = datetime.date(2024, 9, 1)
    guardian_phone = "0501234567"
    is_active      = True


# ── Attendance ────────────────────────────────────────────────────────────────

class AttendanceFactory(DjangoModelFactory):
    class Meta:
        model = Attendance

    student   = factory.SubFactory(StudentFactory)
    date      = factory.LazyFunction(datetime.date.today)
    status    = 'P'
    marked_by = factory.SubFactory(UserFactory)


# ── Academics ─────────────────────────────────────────────────────────────────

class ExamTypeFactory(DjangoModelFactory):
    class Meta:
        model = ExamType
        django_get_or_create = ('name',)

    name              = "MidTerm"
    weight_percentage = 40


class ExamFactory(DjangoModelFactory):
    class Meta:
        model = Exam

    name          = factory.Sequence(lambda n: f"Exam {n}")
    exam_type     = factory.SubFactory(ExamTypeFactory)
    subject       = factory.SubFactory(SubjectFactory)
    section       = factory.SubFactory(SectionFactory)
    academic_year = factory.SubFactory(AcademicYearFactory)
    term          = 'T1'
    date          = datetime.date(2024, 11, 1)
    total_marks   = 100
    created_by    = factory.SubFactory(UserFactory)


class MarkFactory(DjangoModelFactory):
    class Meta:
        model = Mark

    student        = factory.SubFactory(StudentFactory)
    exam           = factory.SubFactory(ExamFactory)
    obtained_marks = 75
    is_absent      = False
    status         = 'draft'
    entered_by     = factory.SubFactory(UserFactory)


# ── Fees ──────────────────────────────────────────────────────────────────────

class FeeTypeFactory(DjangoModelFactory):
    class Meta:
        model = FeeType
        django_get_or_create = ('name',)

    name     = "Tuition"
    category = FeeType.TUITION


class FeeStructureFactory(DjangoModelFactory):
    class Meta:
        model = FeeStructure

    academic_year = factory.SubFactory(AcademicYearFactory)
    grade         = factory.SubFactory(GradeFactory)
    division      = factory.SubFactory(DivisionFactory)
    fee_type      = factory.SubFactory(FeeTypeFactory)
    amount        = factory.LazyFunction(lambda: Decimal('10000.00'))
    due_date      = datetime.date(2024, 10, 1)
    frequency     = "ANNUAL"


class StudentFeeFactory(DjangoModelFactory):
    class Meta:
        model = StudentFee

    student       = factory.SubFactory(StudentFactory)
    fee_structure = factory.SubFactory(FeeStructureFactory)
    amount        = factory.LazyFunction(lambda: Decimal('10000.00'))
    discount      = factory.LazyFunction(lambda: Decimal('0.00'))
    net_amount    = factory.LazyFunction(lambda: Decimal('10000.00'))
    due_date      = datetime.date(2024, 10, 1)
    status        = StudentFee.UNPAID


class PaymentFactory(DjangoModelFactory):
    class Meta:
        model = Payment

    student_fee    = factory.SubFactory(StudentFeeFactory)
    paid_amount    = factory.LazyFunction(lambda: Decimal('5000.00'))
    payment_date   = factory.LazyFunction(datetime.date.today)
    payment_method = 'CASH'
    collected_by   = factory.SubFactory(UserFactory)
