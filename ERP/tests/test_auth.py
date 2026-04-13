"""
Tests for authentication: login, logout, and role-based access control.
"""
import pytest
from django.urls import reverse

from accounts.models import CustomUser
from .factories import UserFactory, TeacherFactory, AccountantFactory


pytestmark = pytest.mark.django_db


# ── Login / Logout ────────────────────────────────────────────────────────────

class TestLogin:
    def test_login_page_renders(self, client):
        url = reverse('accounts:login')
        resp = client.get(url)
        assert resp.status_code == 200

    def test_valid_credentials_redirect_to_dashboard(self, client):
        user = UserFactory(username='admin1', password='TestPass123!')
        resp = client.post(
            reverse('accounts:login'),
            {'username': 'admin1', 'password': 'TestPass123!'},
            follow=True,
        )
        assert resp.status_code == 200
        assert resp.wsgi_request.user.is_authenticated

    def test_wrong_password_stays_on_login(self, client):
        UserFactory(username='admin2', password='TestPass123!')
        resp = client.post(
            reverse('accounts:login'),
            {'username': 'admin2', 'password': 'wrongpassword'},
        )
        assert resp.status_code == 200
        assert not resp.wsgi_request.user.is_authenticated

    def test_inactive_user_cannot_login(self, client):
        user = UserFactory(username='inactive1', password='TestPass123!')
        user.is_active = False
        user.save()
        resp = client.post(
            reverse('accounts:login'),
            {'username': 'inactive1', 'password': 'TestPass123!'},
        )
        assert not resp.wsgi_request.user.is_authenticated

    def test_logout_redirects_to_login(self, client):
        user = UserFactory()
        client.force_login(user)
        resp = client.post(reverse('accounts:logout'), follow=True)
        assert resp.status_code == 200
        assert not resp.wsgi_request.user.is_authenticated


class TestUnauthenticatedRedirect:
    """Unauthenticated requests to protected pages must redirect to login."""

    protected_url_names = [
        'students:list',
        'attendance:take_attendance',
    ]

    @pytest.mark.parametrize("url_name", [
        'students:list',
        'attendance:take',
    ])
    def test_redirect_to_login(self, client, url_name):
        resp = client.get(reverse(url_name))
        assert resp.status_code == 302
        assert '/accounts/login' in resp['Location']


# ── Role-Based Access ─────────────────────────────────────────────────────────

class TestRoleAccess:
    """PARENT role must be denied access to admin-only views."""

    def test_parent_denied_student_add(self, client):
        parent = UserFactory(role=CustomUser.PARENT)
        client.force_login(parent)
        resp = client.get(reverse('students:add'))
        # Should redirect (role_required returns 302 to login or 403)
        assert resp.status_code in (302, 403)

    def test_parent_denied_student_list(self, client):
        parent = UserFactory(role=CustomUser.PARENT)
        client.force_login(parent)
        resp = client.get(reverse('students:list'))
        assert resp.status_code in (302, 403)

    def test_admin_can_access_student_add(self, client):
        admin = UserFactory(role=CustomUser.ADMIN)
        client.force_login(admin)
        resp = client.get(reverse('students:add'))
        assert resp.status_code == 200

    def test_teacher_can_view_student_list(self, client):
        teacher = TeacherFactory()
        client.force_login(teacher)
        resp = client.get(reverse('students:list'))
        assert resp.status_code == 200

    def test_accountant_denied_student_add(self, client):
        acc = AccountantFactory()
        client.force_login(acc)
        resp = client.get(reverse('students:add'))
        assert resp.status_code in (302, 403)
