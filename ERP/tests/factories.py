"""
Shared factory-boy factories for all tests.
Each factory creates a minimal valid object with sensible defaults.
"""
import datetime
from decimal import Decimal
import factory
from factory.django import DjangoModelFactory

from accounts.models import CustomUser
from core.models import AcademicYear, Division, Grade, Section, Subject, StudyMode, Board
from students.models import Student
from attendance.models import Attendance
from academics.models import ExamType, Exam, Mark
from fees.models import (
    FeeType, FeeStructure, FeeStructureItem, StudentFee, Payment, Refund,
    TuitionFeeConfig, PaymentPlan, PaymentPlanInstallment, Salary,
    ExternalCandidate, ExternalCandidatePayment,
)
from staff.models import StaffProfile, TeacherAssignment, VacationRequest, MOEApproval


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


class SuperAdminFactory(UserFactory):
    role = CustomUser.SUPER_ADMIN


class StaffUserFactory(UserFactory):
    role = CustomUser.STAFF


class ParentFactory(UserFactory):
    role = CustomUser.PARENT


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

    # NB: core migration 0005 seeds 'American'; this creates 'AMERICAN' alongside it.
    # Tests that look divisions up with name__iexact must use their own division name.
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


class StudyModeFactory(DjangoModelFactory):
    class Meta:
        model = StudyMode
        django_get_or_create = ('name',)

    name = "On Campus"


class BoardFactory(DjangoModelFactory):
    class Meta:
        model = Board
        django_get_or_create = ('name',)

    name = "IGCSE"


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
    # Keep the hierarchy consistent: section ∈ grade ∈ division
    grade          = factory.SubFactory(GradeFactory, division=factory.SelfAttribute('..division'))
    section        = factory.SubFactory(SectionFactory, grade=factory.SelfAttribute('..grade'))
    academic_year  = factory.SubFactory(AcademicYearFactory)
    admission_date = datetime.date(2024, 9, 1)
    guardian_phone = "0501234567"
    is_active      = True
    id_type        = Student.NATIONAL_ID_TYPE


class ExpatStudentFactory(StudentFactory):
    """Non-Saudi resident (Iqama holder) — attracts 15% VAT on taxable fees."""
    nationality  = "India"
    id_type      = Student.IQAMA
    national_id  = ""
    iqama_number = factory.Sequence(lambda n: f"200000{n:04d}")


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

def _future(days=60):
    return datetime.date.today() + datetime.timedelta(days=days)


class FeeTypeFactory(DjangoModelFactory):
    """Non-taxable by default. Use TaxableFeeTypeFactory for VAT scenarios."""
    class Meta:
        model = FeeType
        django_get_or_create = ('name',)

    name       = "Tuition"
    category   = FeeType.TUITION
    is_taxable = False


class TaxableFeeTypeFactory(FeeTypeFactory):
    name       = "Transport"
    category   = FeeType.TRANSPORT
    is_taxable = True


class FeeStructureFactory(DjangoModelFactory):
    """The container (one per grade / year / structure_type)."""
    class Meta:
        model = FeeStructure

    academic_year  = factory.SubFactory(AcademicYearFactory)
    grade          = factory.SubFactory(GradeFactory)
    structure_type = FeeStructure.TYPE_REGULAR
    frequency      = "ANNUAL"


class FeeStructureItemFactory(DjangoModelFactory):
    """One fee-type line inside a FeeStructure. StudentFee.fee_structure points here."""
    class Meta:
        model = FeeStructureItem

    structure = factory.SubFactory(FeeStructureFactory)
    fee_type  = factory.SubFactory(FeeTypeFactory)
    amount    = factory.LazyFunction(lambda: Decimal('10000.00'))


class StudentFeeFactory(DjangoModelFactory):
    """net_amount is recomputed by StudentFee.save() — don't rely on passing it."""
    class Meta:
        model = StudentFee

    student       = factory.SubFactory(StudentFactory)
    fee_structure = factory.SubFactory(FeeStructureItemFactory)
    amount        = factory.LazyFunction(lambda: Decimal('10000.00'))
    discount      = factory.LazyFunction(lambda: Decimal('0.00'))
    net_amount    = factory.LazyFunction(lambda: Decimal('0.00'))
    due_date      = factory.LazyFunction(_future)
    status        = StudentFee.UNPAID


class PaymentFactory(DjangoModelFactory):
    class Meta:
        model = Payment

    student_fee    = factory.SubFactory(StudentFeeFactory)
    paid_amount    = factory.LazyFunction(lambda: Decimal('5000.00'))
    payment_date   = factory.LazyFunction(datetime.date.today)
    payment_method = Payment.CREDIT_CARD
    collected_by   = factory.SubFactory(UserFactory)


class RefundFactory(DjangoModelFactory):
    class Meta:
        model = Refund

    payment     = factory.SubFactory(PaymentFactory)
    amount      = factory.LazyFunction(lambda: Decimal('1000.00'))
    reason      = "Test refund"
    refunded_by = factory.SubFactory(UserFactory)


class TuitionFeeConfigFactory(DjangoModelFactory):
    class Meta:
        model = TuitionFeeConfig

    academic_year     = factory.SubFactory(AcademicYearFactory)
    division          = factory.SubFactory(DivisionFactory)
    grade             = factory.SubFactory(GradeFactory)
    structure_type    = TuitionFeeConfig.REGULAR
    num_payments      = 2
    gross_tuition_fee = factory.LazyFunction(lambda: Decimal('20000.00'))


class PaymentPlanFactory(DjangoModelFactory):
    class Meta:
        model = PaymentPlan

    student_fee = factory.SubFactory(StudentFeeFactory)


class PaymentPlanInstallmentFactory(DjangoModelFactory):
    class Meta:
        model = PaymentPlanInstallment

    plan           = factory.SubFactory(PaymentPlanFactory)
    installment_no = factory.Sequence(lambda n: n + 1)
    amount         = factory.LazyFunction(lambda: Decimal('5000.00'))
    due_date       = factory.LazyFunction(_future)


class SalaryFactory(DjangoModelFactory):
    class Meta:
        model = Salary

    staff = factory.SubFactory(TeacherFactory)
    month = datetime.date(2025, 9, 1)
    basic = factory.LazyFunction(lambda: Decimal('8000.00'))


class ExternalCandidateFactory(DjangoModelFactory):
    class Meta:
        model = ExternalCandidate

    full_name = factory.Sequence(lambda n: f"Candidate {n}")


class ExternalCandidatePaymentFactory(DjangoModelFactory):
    class Meta:
        model = ExternalCandidatePayment

    candidate       = factory.SubFactory(ExternalCandidateFactory)
    fee_description = "Entrance Exam"
    amount          = factory.LazyFunction(lambda: Decimal('500.00'))


# ── Staff ─────────────────────────────────────────────────────────────────────

class StaffProfileFactory(DjangoModelFactory):
    class Meta:
        model = StaffProfile

    user        = factory.SubFactory(TeacherFactory)
    employee_id = factory.Sequence(lambda n: f"EMP-{n:04d}")
    designation = 'TEACHER'
    department  = 'ACADEMIC'
    join_date   = datetime.date(2023, 8, 1)


class TeacherAssignmentFactory(DjangoModelFactory):
    class Meta:
        model = TeacherAssignment

    teacher       = factory.SubFactory(TeacherFactory)
    subject       = factory.SubFactory(SubjectFactory)
    section       = factory.SubFactory(SectionFactory)
    academic_year = factory.SubFactory(AcademicYearFactory)


class VacationRequestFactory(DjangoModelFactory):
    class Meta:
        model = VacationRequest

    staff     = factory.SubFactory(TeacherFactory)
    from_date = factory.LazyFunction(lambda: _future(10))
    to_date   = factory.LazyFunction(lambda: _future(14))
    reason    = "Family visit"


class MOEApprovalFactory(DjangoModelFactory):
    class Meta:
        model = MOEApproval

    staff         = factory.SubFactory(TeacherFactory)
    approval_type = MOEApproval.TEACHER_LICENSE
