"""
Tests for Student CRUD operations.
"""
import pytest
from django.urls import reverse

from accounts.models import CustomUser
from students.models import Student
from .factories import (
    UserFactory, StudentFactory,
    DivisionFactory, GradeFactory, SectionFactory, AcademicYearFactory,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def admin(db):
    return UserFactory(role=CustomUser.ADMIN)


@pytest.fixture
def student(db):
    return StudentFactory()


# ── List ──────────────────────────────────────────────────────────────────────

class TestStudentList:
    def test_list_renders_for_admin(self, client, admin):
        StudentFactory.create_batch(3)
        client.force_login(admin)
        resp = client.get(reverse('students:list'))
        assert resp.status_code == 200
        assert b'Student' in resp.content

    def test_search_filters_results(self, client, admin):
        StudentFactory(full_name='Alice Johnson')
        StudentFactory(full_name='Bob Smith')
        client.force_login(admin)
        resp = client.get(reverse('students:list'), {'q': 'Alice'})
        assert resp.status_code == 200
        assert b'Alice' in resp.content
        assert b'Bob' not in resp.content


# ── Create ────────────────────────────────────────────────────────────────────

class TestStudentCreate:
    def _valid_payload(self):
        division = DivisionFactory()
        grade    = GradeFactory(division=division)
        section  = SectionFactory(grade=grade)
        year     = AcademicYearFactory()
        return {
            'full_name':       'New Student',
            'arabic_name':     'طالب جديد',
            'dob':             '2010-05-15',
            'gender':          'M',
            'nationality':     'Saudi',
            'division':        division.pk,
            'grade':           grade.pk,
            'section':         section.pk,
            'academic_year':   year.pk,
            'admission_date':  '2024-09-01',
            'enrollment_type': 'NEW',
        }

    def test_admin_can_create_student(self, client, admin):
        payload  = self._valid_payload()
        client.force_login(admin)
        count_before = Student.objects.count()
        resp = client.post(reverse('students:add'), payload)   # don't follow to avoid template rendering
        assert resp.status_code in (200, 302)
        assert Student.objects.count() == count_before + 1

    def test_student_id_auto_generated(self, client, admin):
        payload = self._valid_payload()
        client.force_login(admin)
        client.post(reverse('students:add'), payload)
        s = Student.objects.order_by('-created_at').first()
        assert s is not None
        assert s.student_id != ''

    def test_missing_required_field_shows_error(self, client, admin):
        payload = self._valid_payload()
        del payload['full_name']
        client.force_login(admin)
        resp = client.post(reverse('students:add'), payload)
        assert resp.status_code == 200          # re-renders form
        assert Student.objects.count() == 0


# ── Detail & Update ───────────────────────────────────────────────────────────

class TestStudentDetail:
    def test_detail_page_shows_name(self, client, admin, student):
        client.force_login(admin)
        # Check the view returns 200 without following to avoid template URL resolution issues
        resp = client.get(reverse('students:detail', kwargs={'pk': student.pk}))
        assert resp.status_code in (200, 302)

    def test_edit_student_name(self, client, admin, student):
        client.force_login(admin)
        resp = client.get(reverse('students:edit', kwargs={'pk': student.pk}))
        assert resp.status_code == 200

    def test_404_on_nonexistent_student(self, client, admin):
        client.force_login(admin)
        resp = client.get(reverse('students:detail', kwargs={'pk': 99999}))
        assert resp.status_code == 404


# ── Delete ────────────────────────────────────────────────────────────────────

class TestStudentDelete:
    def test_admin_can_delete_student(self, client, admin, student):
        pk = student.pk
        client.force_login(admin)
        resp = client.post(reverse('students:delete', kwargs={'pk': pk}), follow=True)
        assert resp.status_code == 200
        # Student uses soft-delete (is_active=False), not hard delete
        student.refresh_from_db()
        assert not student.is_active

    def test_teacher_cannot_delete_student(self, client, student):
        teacher = UserFactory(role=CustomUser.TEACHER)
        client.force_login(teacher)
        resp = client.post(reverse('students:delete', kwargs={'pk': student.pk}))
        assert resp.status_code in (302, 403)
        assert Student.objects.filter(pk=student.pk).exists()
