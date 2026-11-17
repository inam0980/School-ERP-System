"""
Unit tests for pure helper functions and the role-based access decorators.
"""
import pytest
from django.contrib.auth.models import AnonymousUser
from django.contrib.messages.storage.fallback import FallbackStorage
from django.http import HttpResponse
from django.test import RequestFactory

from accounts.decorators import role_required, login_excluded
from accounts.models import CustomUser
from fees.views import semester_payment_names, is_semester_fee_name, split_semester_fees


# ── fees.views semester helpers ──────────────────────────────────────────────

class TestSemesterPaymentNames:
    def test_one_payment(self):
        assert semester_payment_names(1) == ['1st Semester']

    def test_two_payments(self):
        assert semester_payment_names(2) == ['1st Semester', '2nd Semester']

    def test_three_payments_puts_two_in_first_semester(self):
        assert semester_payment_names(3) == [
            '1st Semester - 1st Installment',
            '1st Semester - 2nd Installment',
            '2nd Semester',
        ]

    def test_four_payments(self):
        assert semester_payment_names(4) == [
            '1st Semester - 1st Installment', '1st Semester - 2nd Installment',
            '2nd Semester - 1st Installment', '2nd Semester - 2nd Installment',
        ]


class TestIsSemesterFeeName:
    @pytest.mark.parametrize("name, expected", [
        ('1st Semester', True), ('2nd Semester - 1st Installment', True),
        ('3rd Installment', True),            # legacy name
        ('Transport', False), ('Semester Books', False),
    ])
    def test_names(self, name, expected):
        assert is_semester_fee_name(name) is expected


class TestSplitSemesterFees:
    ident = staticmethod(lambda x: x)

    def test_new_style_names(self):
        sem1, sem2 = split_semester_fees(
            ['2nd Semester', 'Transport', '1st Semester'], name_of=self.ident)
        assert sem1 == ['1st Semester'] and sem2 == ['2nd Semester']

    def test_non_tuition_fees_are_dropped(self):
        assert split_semester_fees(['Books', 'Uniform'], name_of=self.ident) == ([], [])

    def test_legacy_names_split_half_half_with_odd_extra_in_sem1(self):
        legacy = ['3rd Installment', '1st Installment', '2nd Installment']
        sem1, sem2 = split_semester_fees(legacy, name_of=self.ident)
        assert sem1 == ['1st Installment', '2nd Installment']
        assert sem2 == ['3rd Installment']


# ── accounts.decorators ──────────────────────────────────────────────────────

def _request(user):
    req = RequestFactory().get('/x/')
    req.user = user
    req.session = {}
    req._messages = FallbackStorage(req)
    return req


@role_required('ADMIN', 'SUPER_ADMIN')
def _admin_view(request):
    return HttpResponse('ok')


@login_excluded()
def _login_view(request):
    return HttpResponse('login form')


class TestRoleRequired:
    def test_anonymous_goes_to_login(self):
        resp = _admin_view(_request(AnonymousUser()))
        assert resp.status_code == 302 and resp.url == '/accounts/login/'

    def test_wrong_role_goes_to_dashboard(self):
        resp = _admin_view(_request(CustomUser(role='TEACHER')))
        assert resp.status_code == 302 and resp.url == '/'

    @pytest.mark.parametrize("role", ['ADMIN', 'SUPER_ADMIN'])
    def test_allowed_role_passes_through(self, role):
        assert _admin_view(_request(CustomUser(role=role))).content == b'ok'

    def test_preserves_function_name(self):
        assert _admin_view.__name__ == '_admin_view'


class TestLoginExcluded:
    def test_authenticated_user_is_redirected(self):
        resp = _login_view(_request(CustomUser(role='ADMIN')))
        assert resp.status_code == 302

    def test_anonymous_sees_view(self):
        assert _login_view(_request(AnonymousUser())).content == b'login form'
