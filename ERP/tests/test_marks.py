"""
Tests for the marks workflow: draft → submitted → approved.
Covers entry, submission, approval, and role restrictions.
"""
import pytest
from django.urls import reverse
from django.utils import timezone

from accounts.models import CustomUser
from academics.models import Mark
from .factories import (
    UserFactory, TeacherFactory,
    ExamFactory, MarkFactory, StudentFactory,
    SectionFactory,
)

pytestmark = pytest.mark.django_db


@pytest.fixture
def admin(db):
    return UserFactory(role=CustomUser.ADMIN)


@pytest.fixture
def teacher(db):
    return TeacherFactory()


@pytest.fixture
def exam(db):
    return ExamFactory()


@pytest.fixture
def student_in_exam(exam):
    """A student whose section matches the exam's section."""
    return StudentFactory(section=exam.section, is_active=True)


# ── Draft entry ───────────────────────────────────────────────────────────────

class TestMarksDraftEntry:
    def test_marks_entry_page_renders(self, client, teacher, exam, student_in_exam):
        client.force_login(teacher)
        resp = client.get(reverse('academics:marks_entry', kwargs={'exam_pk': exam.pk}))
        assert resp.status_code == 200

    def test_teacher_can_save_draft(self, client, teacher, exam, student_in_exam):
        client.force_login(teacher)
        resp = client.post(
            reverse('academics:marks_entry', kwargs={'exam_pk': exam.pk}),
            {
                f'marks_{student_in_exam.pk}': '80',
                f'absent_{student_in_exam.pk}': '',
                f'remarks_{student_in_exam.pk}': '',
                'action': 'draft',
            },
            follow=True,
        )
        assert resp.status_code == 200
        mark = Mark.objects.get(student=student_in_exam, exam=exam)
        assert mark.status == 'draft'
        assert float(mark.obtained_marks) == 80.0

    def test_absent_flag_clears_marks(self, client, teacher, exam, student_in_exam):
        client.force_login(teacher)
        client.post(
            reverse('academics:marks_entry', kwargs={'exam_pk': exam.pk}),
            {
                f'marks_{student_in_exam.pk}': '',
                f'absent_{student_in_exam.pk}': 'on',
                f'remarks_{student_in_exam.pk}': '',
                'action': 'draft',
            },
        )
        mark = Mark.objects.get(student=student_in_exam, exam=exam)
        assert mark.is_absent is True
        assert mark.obtained_marks is None


# ── Submit ────────────────────────────────────────────────────────────────────

class TestMarksSubmit:
    def test_teacher_can_submit_marks(self, client, teacher, exam, student_in_exam):
        client.force_login(teacher)
        client.post(
            reverse('academics:marks_entry', kwargs={'exam_pk': exam.pk}),
            {
                f'marks_{student_in_exam.pk}': '72',
                f'absent_{student_in_exam.pk}': '',
                f'remarks_{student_in_exam.pk}': '',
                'action': 'submit',
            },
        )
        mark = Mark.objects.get(student=student_in_exam, exam=exam)
        assert mark.status == 'submitted'

    def test_submitted_mark_shows_in_approval_queue(self, client, admin, exam):
        MarkFactory(exam=exam, status='submitted')
        client.force_login(admin)
        resp = client.get(reverse('academics:marks_approval'))
        assert resp.status_code == 200


# ── Approve ───────────────────────────────────────────────────────────────────

class TestMarksApprove:
    def test_admin_can_approve_submitted_marks(self, client, admin, exam, student_in_exam):
        mark = MarkFactory(student=student_in_exam, exam=exam, status='submitted')
        client.force_login(admin)
        resp = client.post(
            reverse('academics:approve_marks', kwargs={'exam_pk': exam.pk}),
            follow=True,
        )
        assert resp.status_code == 200
        mark.refresh_from_db()
        assert mark.status == 'approved'
        assert mark.approved_by == admin
        assert mark.approved_at is not None

    def test_teacher_cannot_approve_marks(self, client, teacher, exam, student_in_exam):
        MarkFactory(student=student_in_exam, exam=exam, status='submitted')
        client.force_login(teacher)
        resp = client.post(
            reverse('academics:approve_marks', kwargs={'exam_pk': exam.pk}),
        )
        assert resp.status_code in (302, 403)
        # status must remain 'submitted'
        mark = Mark.objects.get(student=student_in_exam, exam=exam)
        assert mark.status == 'submitted'


# ── Unlock ────────────────────────────────────────────────────────────────────

class TestMarksUnlock:
    def test_admin_can_unlock_approved_marks(self, client, admin, exam, student_in_exam):
        mark = MarkFactory(student=student_in_exam, exam=exam, status='approved')
        client.force_login(admin)
        client.post(reverse('academics:unlock_marks', kwargs={'exam_pk': exam.pk}))
        mark.refresh_from_db()
        assert mark.status == 'submitted'


# ── Percentage & grade helpers ────────────────────────────────────────────────

class TestMarkHelpers:
    def test_get_percentage(self, db):
        mark = MarkFactory.build(obtained_marks=80)
        mark.exam = ExamFactory(total_marks=100)
        assert mark.get_percentage() == 80.0

    def test_absent_has_no_percentage(self, db):
        mark = MarkFactory.build(is_absent=True, obtained_marks=None)
        mark.exam = ExamFactory(total_marks=100)
        assert mark.get_percentage() is None

    def test_letter_grade_a_plus(self, db):
        mark = MarkFactory.build(obtained_marks=95)
        mark.exam = ExamFactory(total_marks=100)
        assert mark.get_letter_grade() == 'A+'
