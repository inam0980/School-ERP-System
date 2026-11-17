"""
Regression tests — one per bug found while bringing the codebase under test.

Each test was written FIRST (red), then the bug was fixed (green).
Never delete a test from this file: it guarantees the bug cannot return.
"""
import datetime
from decimal import Decimal as D

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from accounts.models import CustomUser
from fees.models import StudentFee
from students.models import Student, StudentDocument
from tests import factories as f

pytestmark = [pytest.mark.django_db, pytest.mark.regression]


# ── BUG-01  StudentForm never saved id_type → every expat billed as Saudi (0% VAT)

class TestBug01StudentIdTypeFromForm:
    def _payload(self, school, **ids):
        return {
            'full_name': 'Rahul Kumar', 'arabic_name': 'راهول', 'dob': '2014-03-01',
            'gender': 'M', 'nationality': 'India',
            'division': school.division.pk, 'grade': school.grade.pk,
            'section': school.section.pk, 'academic_year': school.year.pk,
            'admission_date': '2025-09-01', 'enrollment_type': 'NEW',
            'study_mode': school.study_mode.pk, 'fee_category': 'new', 'is_active': 'on',
            **ids,
        }

    def test_student_with_iqama_is_saved_as_non_saudi(self, login, admin, school):
        login(admin).post(reverse('students:add'), self._payload(school, iqama_number='2123456789'))
        s = Student.objects.get(full_name='Rahul Kumar')
        assert s.id_type == Student.IQAMA
        assert s.is_saudi is False

    def test_student_with_national_id_is_saved_as_saudi(self, login, admin, school):
        login(admin).post(reverse('students:add'), self._payload(school, national_id='1123456789'))
        assert Student.objects.get(full_name='Rahul Kumar').id_type == Student.NATIONAL_ID_TYPE

    def test_editing_saudi_to_iqama_updates_id_type(self, login, admin, school):
        s = school.student                                     # created as NATIONAL_ID
        payload = self._payload(school, iqama_number='2999999999')
        payload['full_name'] = s.full_name
        login(admin).post(reverse('students:edit', args=[s.pk]), payload)
        s.refresh_from_db()
        assert s.id_type == Student.IQAMA

    def test_expat_added_through_ui_is_charged_vat(self, login, admin, school):
        login(admin).post(reverse('students:add'), self._payload(school, iqama_number='2123456789'))
        s = Student.objects.get(full_name='Rahul Kumar')
        item = f.FeeStructureItemFactory(fee_type=f.TaxableFeeTypeFactory(), amount=D('1000'))
        fee = f.StudentFeeFactory(student=s, fee_structure=item, amount=D('1000'))
        assert fee.net_amount == D('1150.00')


# ── BUG-02  Open redirect: void/refund honoured next=//evil.com

class TestBug02OpenRedirect:
    @pytest.mark.parametrize("nxt", ['//evil.example.com/phish', 'https://evil.example.com/', '/\\evil.example.com'])
    def test_void_does_not_redirect_offsite(self, login, admin, nxt):
        p = f.PaymentFactory()
        resp = login(admin).post(reverse('fees:void_payment', args=[p.pk]),
                                 {'reason': 'typo', 'next': nxt})
        assert resp.status_code == 302
        assert 'evil.example.com' not in resp['Location']

    def test_void_still_honours_local_next(self, login, admin):
        p = f.PaymentFactory()
        resp = login(admin).post(reverse('fees:void_payment', args=[p.pk]),
                                 {'reason': 'typo', 'next': '/fees/outstanding/'})
        assert resp['Location'] == '/fees/outstanding/'


# ── BUG-03  Fee summary API counted voided payments and was open to every role

class TestBug03FeeSummaryApi:
    def test_voided_payments_not_counted(self, login, accountant):
        f.PaymentFactory(paid_amount=D('1000'))
        f.PaymentFactory(paid_amount=D('400'), is_voided=True)
        data = login(accountant).get(reverse('fees:api_summary')).json()
        assert data['today'] == 1000.0
        assert data['this_month'] == 1000.0

    @pytest.mark.parametrize("role", ['TEACHER', 'STAFF', 'PARENT'])
    def test_non_finance_roles_denied(self, login, role):
        resp = login(f.UserFactory(role=role)).get(reverse('fees:api_summary'))
        assert resp.status_code in (302, 403)


# ── BUG-04  Student search API (returns Iqama numbers) open to every role

class TestBug04StudentSearchApi:
    @pytest.mark.parametrize("role", ['TEACHER', 'STAFF', 'PARENT'])
    def test_non_finance_roles_denied(self, login, school, role):
        resp = login(f.UserFactory(role=role)).get(reverse('fees:student_search_api'), {'q': 'Stu'})
        assert resp.status_code in (302, 403)

    def test_accountant_can_search(self, login, accountant, school):
        data = login(accountant).get(reverse('fees:student_search_api'),
                                     {'q': school.student.full_name[:4]}).json()
        assert any(r['pk'] == school.student.pk for r in data['results'])


# ── BUG-05  Student detail "balance due" counted voided payments & ignored refunds

class TestBug05StudentDetailBalance:
    def test_balance_due_matches_ledger(self, login, admin, school):
        fee = f.StudentFeeFactory(student=school.student, amount=D('10000'))
        f.PaymentFactory(student_fee=fee, paid_amount=D('3000'), is_voided=True)
        live = f.PaymentFactory(student_fee=fee, paid_amount=D('2000'))
        f.RefundFactory(payment=live, amount=D('500'))

        ctx = login(admin).get(reverse('students:detail', args=[school.student.pk])).context
        assert ctx['total_paid'] == D('1500')
        assert ctx['balance_due'] == D('8500')
        assert ctx['balance_due'] == StudentFee.objects.get(pk=fee.pk).balance


# ── BUG-06..09  Pages that crashed with HTTP 500 (found by test_url_sweep)

class TestBug06StudentEditWithDocument:
    def test_edit_page_renders_when_student_has_documents(self, login, admin, school):
        StudentDocument.objects.create(
            student=school.student, doc_type=StudentDocument.PASSPORT,
            file=SimpleUploadedFile('p.pdf', b'%PDF', content_type='application/pdf'))
        resp = login(admin).get(reverse('students:edit', args=[school.student.pk]))
        assert resp.status_code == 200
        assert reverse('students:doc_delete', args=[school.student.documents.first().pk]).encode() in resp.content


class TestBug07VacationList:
    def test_vacation_list_renders_for_staff_without_profile(self, login, admin):
        f.VacationRequestFactory()                      # requester has no StaffProfile
        assert login(admin).get(reverse('staff:vacation_list')).status_code == 200

    def test_links_to_profile_when_one_exists(self, login, admin):
        profile = f.StaffProfileFactory()
        f.VacationRequestFactory(staff=profile.user)
        resp = login(admin).get(reverse('staff:vacation_list'))
        assert reverse('staff:profile', args=[profile.pk]).encode() in resp.content


class TestBug08TuitionConfigForm:
    def test_add_form_renders_all_basic_fields(self, login, admin, school):
        resp = login(admin).get(reverse('fees:tuition_config_add'))
        assert resp.status_code == 200
        for name in ('academic_year', 'division', 'grade', 'structure_type', 'num_payments'):
            assert f'name="{name}"'.encode() in resp.content

    def test_edit_form_renders(self, login, admin, school):
        c = f.TuitionFeeConfigFactory(academic_year=school.year, division=school.division, grade=school.grade)
        assert login(admin).get(reverse('fees:tuition_config_edit', args=[c.pk])).status_code == 200


class TestBug09GradeAnalytics:
    def test_grade_analytics_renders(self, login, admin, school):
        assert login(admin).get(reverse('ai:grade_analytics')).status_code == 200


# ── BUG-10  Attendance API crashed (500) on a bad date or unknown student

class TestBug10AttendanceSubmitValidation:
    url = '/attendance/api/submit/'

    def _post(self, client, payload):
        import json
        return client.post(self.url, data=json.dumps(payload), content_type='application/json')

    def test_invalid_date_returns_400(self, login, teacher, school):
        resp = self._post(login(teacher), {
            'date': '2025-13-45', 'records': [{'student_id': school.student.pk, 'status': 'P'}]})
        assert resp.status_code == 400

    def test_unknown_student_is_skipped_not_500(self, login, teacher, school):
        resp = self._post(login(teacher), {
            'date': '2025-01-10',
            'records': [{'student_id': 999999, 'status': 'P'},
                        {'student_id': school.student.pk, 'status': 'A'}]})
        assert resp.status_code == 200
        assert resp.json()['total'] == 1


# ── BUG-11  IDOR: any logged-in user (incl. PARENT) could open any student's ID card

class TestBug11IdCardAccess:
    def test_parent_cannot_open_arbitrary_id_card(self, login, parent, school):
        resp = login(parent).get(reverse('students:id_card', args=[school.student.pk]))
        assert resp.status_code in (302, 403)

    @pytest.mark.parametrize("role", ['ADMIN', 'TEACHER', 'ACCOUNTANT', 'STAFF'])
    def test_school_staff_can_print_id_card(self, login, school, role):
        resp = login(f.UserFactory(role=role)).get(reverse('students:id_card', args=[school.student.pk]))
        assert resp.status_code == 200


# ── BUG-12  PARENT accounts could file staff vacation requests

class TestBug12VacationRequestsAreForEmployeesOnly:
    @pytest.mark.parametrize("url_name", ['staff:vacation_list', 'staff:vacation_add'])
    def test_parent_denied(self, login, parent, url_name):
        assert login(parent).get(reverse(url_name)).status_code in (302, 403)

    def test_teacher_can_request_leave(self, login, teacher):
        assert login(teacher).get(reverse('staff:vacation_add')).status_code == 200


# ── BUG-15  A plain GET (link prefetch, crawler, double-click) created ZATCA tax invoices

class TestBug15GenerateInvoiceRequiresPost:
    @pytest.fixture
    def paid_fee(self, school):
        fee = f.StudentFeeFactory(student=school.student, amount=D('1000'))
        f.PaymentFactory(student_fee=fee, paid_amount=D('1000'))
        return fee

    def test_get_does_not_create_invoice(self, login, accountant, school, paid_fee):
        from fees.models import TaxInvoice
        resp = login(accountant).get(reverse('fees:generate_invoice', args=[school.student.pk]))
        assert resp.status_code == 405
        assert not TaxInvoice.objects.exists()

    def test_post_creates_invoice(self, login, accountant, school, paid_fee):
        from fees.models import TaxInvoice
        resp = login(accountant).post(reverse('fees:generate_invoice', args=[school.student.pk]))
        assert resp.status_code == 302 and TaxInvoice.objects.count() == 1

    def test_ledger_button_submits_a_post_form(self, login, accountant, school):
        resp = login(accountant).get(reverse('fees:student_ledger', args=[school.student.pk]))
        html = resp.content.decode()
        url = reverse('fees:generate_invoice', args=[school.student.pk])
        assert f'action="{url}"' in html and 'method="post"' in html.lower()


# ── BUG-16  Open redirect after login: /accounts/login/?next=https://evil.example.com

class TestBug16LoginOpenRedirect:
    @pytest.mark.parametrize("nxt", ['https://evil.example.com/', '//evil.example.com', '/\evil.example.com'])
    def test_offsite_next_is_ignored(self, client, nxt):
        f.UserFactory(username='u16', password='Pass-Word-1616')
        resp = client.post(f"{reverse('accounts:login')}?next={nxt}",
                           {'username': 'u16', 'password': 'Pass-Word-1616'})
        assert resp.status_code == 302 and 'evil.example.com' not in resp['Location']

    def test_local_next_is_honoured(self, client):
        f.UserFactory(username='u16', password='Pass-Word-1616')
        resp = client.post(f"{reverse('accounts:login')}?next=/fees/",
                           {'username': 'u16', 'password': 'Pass-Word-1616'})
        assert resp['Location'] == '/fees/'


# ── BUG-17  Top bar showed the username: it used user.first_name / get_full_name,
#            which CustomUser does not have

class TestBug17HeaderShowsFullName:
    def test_header_shows_full_name_not_username(self, login):
        u = f.UserFactory(username='zz_login_name', full_name='Fatima Al-Harbi', role='ADMIN')
        html = login(u).get(reverse('students:hub')).content.decode()   # page body never names the user
        assert 'Fatima Al-Harbi' in html
        assert 'zz_login_name' not in html


# ── BUG-18  Every CSV export put a hidden BOM (﻿) at the start of EVERY row:
#            charset=utf-8-sig adds one per write. Corrupts the first column
#            (student IDs, receipt nos.) — including the Noor file sent to the Ministry.

BOM = '﻿'.encode('utf-8')


class TestBug18CsvExportsHaveExactlyOneBom:
    @pytest.fixture
    def data(self, school):
        import datetime
        from academics.models import Mark  # noqa: F401
        overdue = f.StudentFeeFactory(student=school.student, amount=D('1000'),
                                      due_date=datetime.date.today() - datetime.timedelta(days=5))
        overdue.refresh_status()
        f.StudentFeeFactory(student=school.expat, amount=D('500'),
                            due_date=datetime.date.today() - datetime.timedelta(days=5)).refresh_status()
        from fees.models import FeeType
        uniform = f.FeeTypeFactory(name='Uniform', category=FeeType.UNIFORM)       # → sales report
        paid = f.StudentFeeFactory(student=school.expat, amount=D('300'),
                                   fee_structure=f.FeeStructureItemFactory(fee_type=uniform))
        f.PaymentFactory(student_fee=paid, paid_amount=D('100'))
        f.PaymentFactory(student_fee=paid, paid_amount=D('50'))
        sem1 = f.FeeTypeFactory(name='1st Semester', category=FeeType.TUITION)     # → unpaid tuition
        for s in (school.student, school.expat):
            f.StudentFeeFactory(student=s, amount=D('9000'), fee_structure=f.FeeStructureItemFactory(
                fee_type=sem1, structure=f.FeeStructureFactory(academic_year=school.year, grade=school.grade,
                                                               structure_type='new' if s is school.expat else 'regular')))
        f.SalaryFactory(month=datetime.date.today().replace(day=1))
        f.SalaryFactory(staff=f.AccountantFactory(), month=datetime.date.today().replace(day=1))
        f.TuitionFeeConfigFactory(academic_year=school.year, division=school.division, grade=school.grade)
        exam = f.ExamFactory(section=school.section, subject=school.subject, academic_year=school.year, term='T1')
        for s in (school.student, school.expat):
            f.MarkFactory(student=s, exam=exam, obtained_marks=70, status='approved')
        return school

    @pytest.mark.parametrize("url_name, params", [
        ('fees:outstanding',            {'export': 'csv'}),
        ('fees:unpaid_tuition',         {'export': 'csv'}),
        ('fees:sales_report',           {'export': 'csv'}),
        ('fees:daily_collection',       {'export': 'csv'}),
        ('fees:defaulters',             {'export': 'csv'}),
        ('fees:payroll_list',           {'export': 'csv'}),
        ('fees:tuition_config_export_csv', {}),
        ('academics:noor_export',       'NOOR'),
    ])
    def test_single_leading_bom(self, login, super_admin, data, url_name, params):
        if params == 'NOOR':
            params = {'section': data.section.pk, 'year': data.year.pk, 'term': 'T1'}
        resp = login(super_admin).get(reverse(url_name), params)
        assert resp.status_code == 200 and 'csv' in resp['Content-Type']
        body = resp.content
        assert body.count(b'\n') >= 2, "fixture should produce at least a header + one data row"
        assert body.startswith(BOM), "keep one BOM so Excel shows Arabic correctly"
        assert body.count(BOM) == 1, f"{body.count(BOM)} BOMs found — rows are corrupted"
