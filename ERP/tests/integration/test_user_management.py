"""
User account management (accounts app).

Before this feature the only way to create a login for a teacher/accountant, or
reset a forgotten password, was Django's hidden /admin/ panel.
"""
import pytest
from django.urls import reverse

from accounts.models import CustomUser
from tests import factories as f

pytestmark = pytest.mark.django_db

STRONG = 'Kawthar-2026-secure!'


def _new_user_payload(**over):
    data = {'username': 'sara.t', 'full_name': 'Sara Teacher', 'email': 'sara@school.sa',
            'role': 'TEACHER', 'password1': STRONG, 'password2': STRONG}
    data.update(over)
    return data


# ── Access ───────────────────────────────────────────────────────────────────

class TestAccess:
    @pytest.mark.parametrize("url_name", ['accounts:user_list', 'accounts:user_add'])
    @pytest.mark.parametrize("role", ['TEACHER', 'ACCOUNTANT', 'STAFF', 'PARENT'])
    def test_non_admins_denied(self, login, role, url_name):
        assert login(f.UserFactory(role=role)).get(reverse(url_name)).status_code in (302, 403)

    @pytest.mark.parametrize("role", ['ADMIN', 'SUPER_ADMIN'])
    def test_admins_see_user_list(self, login, role):
        other = f.TeacherFactory(full_name='Visible Teacher')
        resp = login(f.UserFactory(role=role)).get(reverse('accounts:user_list'))
        assert resp.status_code == 200 and other in resp.context['users']

    def test_list_filters_by_role_and_search(self, login, admin):
        t = f.TeacherFactory(full_name='Omar Haddad')
        a = f.AccountantFactory(full_name='Omar Accountant')
        client = login(admin)
        assert list(client.get(reverse('accounts:user_list'), {'role': 'TEACHER'}).context['users']) == [t]
        found = client.get(reverse('accounts:user_list'), {'q': 'Accountant'}).context['users']
        assert list(found) == [a]


# ── Create ───────────────────────────────────────────────────────────────────

class TestCreateUser:
    def test_admin_creates_teacher_who_can_then_log_in(self, login, admin, client):
        resp = login(admin).post(reverse('accounts:user_add'), _new_user_payload())
        assert resp.status_code == 302
        u = CustomUser.objects.get(username='sara.t')
        assert (u.role, u.full_name, u.is_active) == ('TEACHER', 'Sara Teacher', True)
        assert u.check_password(STRONG)
        client.logout()
        assert client.login(username='sara.t', password=STRONG)

    def test_passwords_must_match(self, login, admin):
        login(admin).post(reverse('accounts:user_add'), _new_user_payload(password2='other-Pass-99'))
        assert not CustomUser.objects.filter(username='sara.t').exists()

    @pytest.mark.parametrize("weak", ['12345678', 'password', 'short'])
    def test_weak_passwords_rejected(self, login, admin, weak):
        resp = login(admin).post(reverse('accounts:user_add'),
                                 _new_user_payload(password1=weak, password2=weak))
        assert resp.status_code == 200
        assert not CustomUser.objects.filter(username='sara.t').exists()

    def test_duplicate_username_and_email_rejected(self, login, admin):
        f.UserFactory(username='sara.t', email='sara@school.sa')
        resp = login(admin).post(reverse('accounts:user_add'), _new_user_payload())
        form = resp.context['form']
        assert 'username' in form.errors and 'email' in form.errors

    def test_admin_cannot_create_super_admin(self, login, admin):
        login(admin).post(reverse('accounts:user_add'), _new_user_payload(role='SUPER_ADMIN'))
        assert not CustomUser.objects.filter(username='sara.t').exists()

    def test_super_admin_can_create_super_admin(self, login, super_admin):
        login(super_admin).post(reverse('accounts:user_add'), _new_user_payload(role='SUPER_ADMIN'))
        assert CustomUser.objects.get(username='sara.t').role == 'SUPER_ADMIN'

    def test_new_user_appears_in_staff_profile_form(self, login, admin):
        """The staff module needs an existing user — this closes that loop."""
        login(admin).post(reverse('accounts:user_add'), _new_user_payload())
        resp = login(admin).get(reverse('staff:staff_add'))
        assert CustomUser.objects.get(username='sara.t') in resp.context['form'].fields['user'].queryset


# ── Edit ─────────────────────────────────────────────────────────────────────

class TestEditUser:
    def test_admin_changes_role_and_name(self, login, admin):
        t = f.TeacherFactory()
        login(admin).post(reverse('accounts:user_edit', args=[t.pk]),
                          {'full_name': 'Renamed', 'email': t.email, 'role': 'ACCOUNTANT'})
        t.refresh_from_db()
        assert (t.full_name, t.role) == ('Renamed', 'ACCOUNTANT')

    def test_edit_does_not_touch_password(self, login, admin):
        t = f.TeacherFactory(password='Original-Pass-77')
        login(admin).post(reverse('accounts:user_edit', args=[t.pk]),
                          {'full_name': 'X', 'email': t.email, 'role': 'TEACHER'})
        t.refresh_from_db()
        assert t.check_password('Original-Pass-77')

    def test_admin_cannot_edit_super_admin(self, login, admin, super_admin):
        resp = login(admin).post(reverse('accounts:user_edit', args=[super_admin.pk]),
                                 {'full_name': 'Hacked', 'email': super_admin.email, 'role': 'STAFF'})
        assert resp.status_code in (302, 403)
        super_admin.refresh_from_db()
        assert super_admin.role == 'SUPER_ADMIN' and super_admin.full_name != 'Hacked'

    def test_admin_cannot_promote_anyone_to_super_admin(self, login, admin):
        t = f.TeacherFactory()
        login(admin).post(reverse('accounts:user_edit', args=[t.pk]),
                          {'full_name': t.full_name, 'email': t.email, 'role': 'SUPER_ADMIN'})
        t.refresh_from_db()
        assert t.role == 'TEACHER'

    def test_cannot_change_own_role(self, login, admin):
        login(admin).post(reverse('accounts:user_edit', args=[admin.pk]),
                          {'full_name': admin.full_name, 'email': admin.email, 'role': 'STAFF'})
        admin.refresh_from_db()
        assert admin.role == 'ADMIN'


# ── Activate / deactivate ────────────────────────────────────────────────────

class TestToggleActive:
    def test_deactivated_user_cannot_log_in(self, login, admin, client):
        t = f.TeacherFactory(username='leaver', password=STRONG)
        login(admin).post(reverse('accounts:user_toggle_active', args=[t.pk]))
        t.refresh_from_db()
        assert not t.is_active
        client.logout()
        assert not client.login(username='leaver', password=STRONG)

    def test_toggle_reactivates(self, login, admin):
        t = f.TeacherFactory(is_active=False)
        login(admin).post(reverse('accounts:user_toggle_active', args=[t.pk]))
        t.refresh_from_db()
        assert t.is_active

    def test_cannot_deactivate_yourself(self, login, admin):
        login(admin).post(reverse('accounts:user_toggle_active', args=[admin.pk]))
        admin.refresh_from_db()
        assert admin.is_active

    def test_last_super_admin_cannot_be_deactivated(self, login, super_admin):
        other_sa = f.SuperAdminFactory()
        client = login(super_admin)
        client.post(reverse('accounts:user_toggle_active', args=[other_sa.pk]))   # fine, one left
        other_sa.refresh_from_db()
        assert not other_sa.is_active
        assert CustomUser.objects.filter(role='SUPER_ADMIN', is_active=True).count() == 1

    def test_admin_cannot_deactivate_super_admin(self, login, admin, super_admin):
        login(admin).post(reverse('accounts:user_toggle_active', args=[super_admin.pk]))
        super_admin.refresh_from_db()
        assert super_admin.is_active

    def test_get_not_allowed(self, login, admin):
        t = f.TeacherFactory()
        assert login(admin).get(reverse('accounts:user_toggle_active', args=[t.pk])).status_code == 405


# ── Passwords ────────────────────────────────────────────────────────────────

class TestAdminResetPassword:
    def test_admin_resets_forgotten_password(self, login, admin, client):
        t = f.TeacherFactory(username='forgetful')
        login(admin).post(reverse('accounts:user_reset_password', args=[t.pk]),
                          {'new_password1': STRONG, 'new_password2': STRONG})
        client.logout()
        assert client.login(username='forgetful', password=STRONG)

    def test_weak_reset_rejected(self, login, admin):
        t = f.TeacherFactory(password='Original-Pass-77')
        login(admin).post(reverse('accounts:user_reset_password', args=[t.pk]),
                          {'new_password1': '123', 'new_password2': '123'})
        t.refresh_from_db()
        assert t.check_password('Original-Pass-77')

    def test_admin_cannot_reset_super_admin_password(self, login, admin, super_admin):
        login(admin).post(reverse('accounts:user_reset_password', args=[super_admin.pk]),
                          {'new_password1': STRONG, 'new_password2': STRONG})
        super_admin.refresh_from_db()
        assert not super_admin.check_password(STRONG)


class TestChangeOwnPassword:
    @pytest.mark.parametrize("role", ['TEACHER', 'ACCOUNTANT', 'STAFF', 'PARENT', 'ADMIN'])
    def test_any_user_changes_own_password_and_stays_logged_in(self, login, role):
        u = f.UserFactory(role=role, password='Old-Pass-2024!')
        client = login(u)
        resp = client.post(reverse('accounts:password_change'), {
            'old_password': 'Old-Pass-2024!', 'new_password1': STRONG, 'new_password2': STRONG})
        assert resp.status_code == 302
        u.refresh_from_db()
        assert u.check_password(STRONG)
        assert client.get(reverse('accounts:profile')).status_code == 200    # session kept

    def test_wrong_old_password_rejected(self, login, teacher):
        login(teacher).post(reverse('accounts:password_change'), {
            'old_password': 'nope', 'new_password1': STRONG, 'new_password2': STRONG})
        teacher.refresh_from_db()
        assert not teacher.check_password(STRONG)

    def test_anonymous_redirected(self, client):
        assert client.get(reverse('accounts:password_change')).status_code == 302


# ── No parent portal (school decision 2026-11-17): PARENT accounts can't be created

class TestParentRoleHidden:
    @pytest.mark.parametrize("actor_role", ['ADMIN', 'SUPER_ADMIN'])
    def test_parent_not_offered(self, login, actor_role):
        form = login(f.UserFactory(role=actor_role)).get(reverse('accounts:user_add')).context['form']
        assert 'PARENT' not in [c[0] for c in form.fields['role'].choices]

    def test_parent_cannot_be_posted(self, login, super_admin):
        login(super_admin).post(reverse('accounts:user_add'), _new_user_payload(role='PARENT'))
        assert not CustomUser.objects.filter(username='sara.t').exists()
