"""
URL sweep — the safety net for the whole application.

For EVERY named route and EVERY user role, issue a GET and assert:
  1. the server never crashes (no exception / 500), and
  2. a GET never deletes or changes data (delete endpoints must require POST), and
  3. role-based access matches the access matrix below.

A new URL added to any urls.py is picked up automatically. If it needs an
object id, add it to `ROUTE_OBJECTS` below — the test fails loudly until you do.
"""
import datetime
from decimal import Decimal as D

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import URLPattern, URLResolver, get_resolver, reverse

from academics.models import GradeConfig
from accounts.models import CustomUser
from fees.models import TaxInvoice, TuitionInstallment
from students.models import AuthorizedPickup, Sibling, StudentDocument
from tests import factories as f

pytestmark = pytest.mark.django_db

SKIP_NAMESPACES = {'admin'}
# Logout is POST-only and ends the session — covered in test_auth.py.
# protected_media takes a file path, not a pk — covered in test_security_settings.py.
SKIP_ROUTES = {'accounts:logout', 'protected_media'}


def _all_routes():
    out = []

    def walk(patterns, ns=None):
        for p in patterns:
            if isinstance(p, URLResolver):
                walk(p.url_patterns, p.namespace or ns)
            elif isinstance(p, URLPattern) and p.name and ns not in SKIP_NAMESPACES:
                # path() exposes params as converters; re_path() only as regex groups.
                params = list(p.pattern.converters) or list(p.pattern.regex.groupindex)
                out.append((f"{ns}:{p.name}" if ns else p.name, params))
    walk(get_resolver().url_patterns)
    return sorted(set((n, tuple(k)) for n, k in out))


ROUTES = _all_routes()


# ── One of everything ────────────────────────────────────────────────────────

@pytest.fixture
def world(db, school):
    w = school
    w.admin_user = f.UserFactory(role=CustomUser.ADMIN)
    w.exam_type = f.ExamTypeFactory()
    w.exam = f.ExamFactory(exam_type=w.exam_type, subject=w.subject, section=w.section,
                           academic_year=w.year, created_by=w.admin_user)
    f.MarkFactory(student=w.student, exam=w.exam, entered_by=w.admin_user)
    f.AttendanceFactory(student=w.student, marked_by=w.admin_user)
    w.board = f.BoardFactory()
    w.grade_config = GradeConfig.objects.create(grade=w.grade)

    w.document = StudentDocument.objects.create(
        student=w.student, doc_type=StudentDocument.PASSPORT,
        file=SimpleUploadedFile('passport.pdf', b'%PDF-1.4 test', content_type='application/pdf'))
    w.sibling = Sibling.objects.create(student=w.student, full_name='Sib', relation=Sibling.BROTHER)
    w.pickup = AuthorizedPickup.objects.create(student=w.student, full_name='Uncle', relation='Uncle', phone='050')

    w.fee_type = f.FeeTypeFactory()
    w.structure = f.FeeStructureFactory(academic_year=w.year, grade=w.grade)
    w.item = f.FeeStructureItemFactory(structure=w.structure, fee_type=w.fee_type)
    w.student_fee = f.StudentFeeFactory(student=w.student, fee_structure=w.item)
    w.payment = f.PaymentFactory(student_fee=w.student_fee, paid_amount=D('1000'),
                                 collected_by=w.admin_user)
    w.plan = f.PaymentPlanFactory(student_fee=w.student_fee)
    f.PaymentPlanInstallmentFactory(plan=w.plan)
    w.invoice = TaxInvoice.objects.create(student=w.student, subtotal=D('100'), total=D('100'))
    w.salary = f.SalaryFactory()
    w.tuition = f.TuitionFeeConfigFactory(academic_year=w.year, division=w.division, grade=w.grade)
    TuitionInstallment.objects.create(config=w.tuition, installment_type='FIRST', amount=D('10000'))
    w.candidate = f.ExternalCandidateFactory(grade_applying=w.grade, division=w.division)

    w.staff_profile = f.StaffProfileFactory()
    w.assignment = f.TeacherAssignmentFactory(subject=w.subject, section=w.section, academic_year=w.year)
    w.vacation = f.VacationRequestFactory()
    w.moe = f.MOEApprovalFactory()
    w.other_user = f.TeacherFactory()
    return w


# url-name → attribute on `world` whose pk fills the single URL kwarg
ROUTE_OBJECTS = {
    'core:academic_year_edit': 'year', 'core:academic_year_delete': 'year',
    'core:division_edit': 'division', 'core:division_delete': 'division',
    'core:grade_edit': 'grade', 'core:grade_delete': 'grade',
    'core:section_edit': 'section', 'core:section_delete': 'section',
    'core:subject_edit': 'subject', 'core:subject_delete': 'subject',
    'core:board_edit': 'board', 'core:board_delete': 'board',
    'core:study_mode_edit': 'study_mode', 'core:study_mode_delete': 'study_mode',

    'students:detail': 'student', 'students:edit': 'student', 'students:delete': 'student',
    'students:doc_upload': 'student', 'students:sibling_add': 'student',
    'students:pickup_add': 'student', 'students:id_card': 'student',
    'students:continuation_agreement': 'student', 'students:enrollment_contract': 'student',
    'students:promotion_individual': 'student',
    'students:doc_delete': 'document', 'students:sibling_delete': 'sibling',
    'students:pickup_delete': 'pickup',
    'students:external_detail': 'candidate', 'students:external_edit': 'candidate',

    'attendance:student_calendar': 'student',

    'academics:exam_type_edit': 'exam_type', 'academics:exam_type_delete': 'exam_type',
    'academics:exam_edit': 'exam', 'academics:exam_delete': 'exam',
    'academics:marks_entry': 'exam', 'academics:approve_marks': 'exam',
    'academics:unlock_marks': 'exam', 'academics:exam_results': 'exam',
    'academics:export_marks': 'exam',
    'academics:report_card': 'student', 'academics:report_card_pdf': 'student',
    'academics:grade_config_edit': 'grade_config',

    'fees:fee_type_edit': 'fee_type', 'fees:fee_type_delete': 'fee_type',
    'fees:fee_structure_edit': 'structure', 'fees:fee_structure_delete': 'structure',
    'fees:fee_structure_items': 'structure',
    'fees:assign_student_fee': 'student', 'fees:student_ledger': 'student',
    'fees:generate_invoice': 'student',
    'fees:student_fee_edit': 'student_fee', 'fees:payment_plan_setup': 'student_fee',
    'fees:payment_plan_delete': 'plan',
    'fees:receipt_print': 'payment', 'fees:void_payment': 'payment',
    'fees:refund_payment': 'payment', 'fees:bank_verify': 'payment',
    'fees:invoice_print': 'invoice',
    'fees:salary_edit': 'salary', 'fees:salary_delete': 'salary', 'fees:salary_mark_paid': 'salary',
    'fees:tuition_config_detail': 'tuition', 'fees:tuition_config_edit': 'tuition',
    'fees:tuition_config_delete': 'tuition', 'fees:tuition_config_print': 'tuition',

    'staff:profile': 'staff_profile', 'staff:staff_edit': 'staff_profile',
    'staff:staff_delete': 'staff_profile',
    'staff:teacher_assignment_edit': 'assignment', 'staff:teacher_assignment_delete': 'assignment',
    'staff:vacation_edit': 'vacation', 'staff:vacation_approve': 'vacation',
    'staff:moe_edit': 'moe', 'staff:moe_delete': 'moe',

    'ai:performance_summary': 'student',

    'accounts:user_edit': 'other_user', 'accounts:user_reset_password': 'other_user',
    'accounts:user_toggle_active': 'other_user',
}


def _url(name, kwargs, world):
    if not kwargs:
        return reverse(name)
    assert name in ROUTE_OBJECTS, (
        f"New parameterised route '{name}' — add it to ROUTE_OBJECTS in test_url_sweep.py")
    obj = getattr(world, ROUTE_OBJECTS[name])
    return reverse(name, kwargs={kwargs[0]: obj.pk})


def test_every_parameterised_route_is_mapped():
    unmapped = [n for n, k in ROUTES if k and n not in ROUTE_OBJECTS and n not in SKIP_ROUTES]
    assert not unmapped, f"Add these to ROUTE_OBJECTS: {unmapped}"


# ── 1 + 2: never crash, never mutate on GET ──────────────────────────────────

ROLES = [r for r, _ in CustomUser.ROLE_CHOICES]


@pytest.mark.parametrize("role", ROLES)
def test_no_route_crashes_and_get_never_deletes(client, world, role):
    from django.apps import apps

    def snapshot():
        return {m._meta.label: m.objects.count() for m in apps.get_models()
                if m._meta.app_label in {'core', 'students', 'academics', 'attendance',
                                         'fees', 'staff', 'accounts'}}

    client.force_login(f.UserFactory(role=role))
    before = snapshot()
    failures = []
    for name, kwargs in ROUTES:
        if name in SKIP_ROUTES:
            continue
        url = _url(name, kwargs, world)
        try:
            resp = client.get(url)
        except Exception as exc:                                   # noqa: BLE001
            failures.append(f"{name} {url} → {type(exc).__name__}: {exc}"[:300])
            continue
        if resp.status_code >= 500:
            failures.append(f"{name} {url} → HTTP {resp.status_code}")
    after = snapshot()
    changed = {k: (before[k], after[k]) for k in before if before[k] != after[k]}

    # Users are created only by force_login above — ignore that table.
    changed.pop('accounts.CustomUser', None)
    assert not failures, "\n".join(failures)
    assert not changed, f"GET requests changed data: {changed}"


# ── 3: access matrix ─────────────────────────────────────────────────────────

# Routes any authenticated user (incl. PARENT) may open — reviewed and accepted.
# Adding a route here is a security decision: write the reason next to it.
PUBLIC_TO_LOGGED_IN = {
    'core:dashboard', 'accounts:profile', 'accounts:login',
    # Every user must be able to change their own password.
    'accounts:password_change',
    # Dropdown reference data (names of grades/sections/subjects) — no PII.
    'core:api_grades', 'core:api_sections', 'core:api_study_modes',
    'academics:api_subjects', 'academics:api_exams',
    # School-wide aggregate counts shown on the shared dashboard — no PII.
    'attendance:api_summary',
}

# Finance routes deliberately opened to STAFF via fees.views._STAFF_VIEW (price lists only).
FINANCE_OPEN_TO_STAFF = {'fees:fee_structure_export_csv', 'fees:fee_structure_export_group_csv'}


@pytest.mark.parametrize("role", ['PARENT'])
def test_parent_cannot_open_internal_pages(client, world, role):
    """The PARENT role has no back-office access. Anything that renders is a data leak."""
    client.force_login(f.UserFactory(role=role))
    leaks = []
    for name, kwargs in ROUTES:
        if name in SKIP_ROUTES or name in PUBLIC_TO_LOGGED_IN:
            continue
        resp = client.get(_url(name, kwargs, world))
        if resp.status_code == 200:
            leaks.append(name)
    assert not leaks, f"PARENT can open: {leaks}"


@pytest.mark.parametrize("role", ['TEACHER', 'STAFF'])
def test_non_finance_roles_cannot_open_finance_pages(client, world, role):
    client.force_login(f.UserFactory(role=role))
    leaks = []
    for name, kwargs in ROUTES:
        if not name.startswith('fees:') or name in SKIP_ROUTES:
            continue
        if role == 'STAFF' and name in FINANCE_OPEN_TO_STAFF:
            continue
        resp = client.get(_url(name, kwargs, world))
        if resp.status_code == 200:
            leaks.append(name)
    assert not leaks, f"{role} can open finance pages: {leaks}"


def test_anonymous_is_always_sent_to_login(client, world):
    leaks = []
    for name, kwargs in ROUTES:
        if name in SKIP_ROUTES or name == 'accounts:login':
            continue
        resp = client.get(_url(name, kwargs, world))
        if resp.status_code == 200:
            leaks.append(name)
    assert not leaks, f"Anonymous users can open: {leaks}"
