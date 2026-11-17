"""
End-to-end academic workflows: promotion, attendance marking, marks locking.
"""
import datetime
import json

import pytest
from django.urls import reverse

from academics.models import Mark
from attendance.models import Attendance
from students.models import PromotionHistory, Student
from tests import factories as f

pytestmark = pytest.mark.django_db


@pytest.fixture
def next_year_setup(school):
    """Next academic year + the next grade (with a section) in the same division."""
    ny = f.AcademicYearFactory(name='2025-26', start_date=datetime.date(2025, 9, 1),
                               end_date=datetime.date(2026, 6, 30), is_current=False)
    g2 = f.GradeFactory(division=school.division, order=2, name='Grade 2')
    s2 = f.SectionFactory(grade=g2, name='A')
    return ny, g2, s2


# ── Promotion ────────────────────────────────────────────────────────────────

class TestIndividualPromotion:
    def test_get_suggests_next_grade(self, login, admin, school, next_year_setup):
        _, g2, _ = next_year_setup
        resp = login(admin).get(reverse('students:promotion_individual', args=[school.student.pk]))
        assert resp.context['suggested_grade'] == g2

    def test_promote_moves_student_and_writes_history(self, login, admin, school, next_year_setup):
        ny, g2, s2 = next_year_setup
        s = school.student
        login(admin).post(reverse('students:promotion_individual', args=[s.pk]), {
            'action': 'PROMOTE', 'to_academic_year': ny.pk, 'to_division': school.division.pk,
            'to_grade': g2.pk, 'to_section': s2.pk, 'notes': 'Good year'})
        s.refresh_from_db()
        assert (s.academic_year, s.grade, s.section) == (ny, g2, s2)
        assert s.enrollment_type == Student.REGULAR
        h = PromotionHistory.objects.get(student=s)
        assert h.action == 'PROMOTE' and h.from_grade == school.grade and h.to_grade == g2
        assert h.promoted_by == admin

    def test_transfer_out_deactivates(self, login, admin, school):
        s = school.student
        login(admin).post(reverse('students:promotion_individual', args=[s.pk]), {'action': 'TRANSFER_OUT'})
        s.refresh_from_db()
        assert not s.is_active
        assert PromotionHistory.objects.get(student=s).to_grade is None

    def test_section_from_another_grade_is_rejected(self, login, admin, school, next_year_setup):
        ny, g2, _ = next_year_setup
        s = school.student
        resp = login(admin).post(reverse('students:promotion_individual', args=[s.pk]), {
            'action': 'PROMOTE', 'to_academic_year': ny.pk, 'to_division': school.division.pk,
            'to_grade': g2.pk, 'to_section': school.section.pk})          # section ∉ g2
        assert resp.status_code == 200
        s.refresh_from_db()
        assert s.grade == school.grade and not PromotionHistory.objects.exists()


class TestBulkPromotion:
    def _post(self, client, school, setup, ids, **overrides):
        ny, g2, s2 = setup
        data = {'student_ids': ids, 'default_to_academic_year': ny.pk,
                'default_to_division': school.division.pk, 'default_to_grade': g2.pk}
        for sid in ids:
            data[f'action_{sid}'] = 'PROMOTE'
            data[f'to_section_{sid}'] = s2.pk
        data.update(overrides)
        return client.post(reverse('students:promotion_bulk'), data)

    def test_bulk_promotes_everyone(self, login, admin, school, next_year_setup):
        ids = [school.student.pk, school.expat.pk]
        self._post(login(admin), school, next_year_setup, ids)
        assert Student.objects.filter(pk__in=ids, grade=next_year_setup[1]).count() == 2
        assert PromotionHistory.objects.count() == 2

    def test_one_bad_row_rolls_back_whole_batch(self, login, admin, school, next_year_setup):
        """Atomicity: a half-promoted class is worse than none."""
        ids = [school.student.pk, school.expat.pk]
        self._post(login(admin), school, next_year_setup, ids,
                   **{f'to_section_{school.expat.pk}': school.section.pk})   # wrong grade
        assert not PromotionHistory.objects.exists()
        assert Student.objects.filter(pk__in=ids, grade=school.grade).count() == 2


# ── Attendance ───────────────────────────────────────────────────────────────

class TestAttendanceSubmit:
    url = '/attendance/api/submit/'

    def _post(self, client, payload):
        return client.post(self.url, data=json.dumps(payload), content_type='application/json')

    def test_teacher_marks_class(self, login, teacher, school):
        resp = self._post(login(teacher), {'date': '2025-01-12', 'records': [
            {'student_id': school.student.pk, 'status': 'P'},
            {'student_id': school.expat.pk, 'status': 'A', 'remarks': 'sick'}]})
        assert resp.json() == {'success': True, 'created': 2, 'updated': 0, 'total': 2, 'date': '2025-01-12'}
        assert Attendance.objects.get(student=school.expat).remarks == 'sick'

    def test_resubmission_updates_instead_of_duplicating(self, login, teacher, school):
        client = login(teacher)
        payload = {'date': '2025-01-12', 'records': [{'student_id': school.student.pk, 'status': 'P'}]}
        self._post(client, payload)
        payload['records'][0]['status'] = 'L'
        assert self._post(client, payload).json()['updated'] == 1
        assert Attendance.objects.get().status == 'L'

    def test_invalid_status_is_ignored(self, login, teacher, school):
        resp = self._post(login(teacher), {'date': '2025-01-12', 'records': [
            {'student_id': school.student.pk, 'status': 'X'}]})
        assert resp.json()['total'] == 0

    @pytest.mark.parametrize("body", ['not json', json.dumps({'records': []}), json.dumps({'date': '2025-01-01'})])
    def test_malformed_body_is_400(self, login, teacher, body):
        resp = login(teacher).post(self.url, data=body, content_type='application/json')
        assert resp.status_code == 400

    def test_accountant_cannot_mark(self, login, accountant, school):
        resp = self._post(login(accountant), {'date': '2025-01-12', 'records': [
            {'student_id': school.student.pk, 'status': 'P'}]})
        assert resp.status_code in (302, 403)
        assert not Attendance.objects.exists()


# ── Marks locking ────────────────────────────────────────────────────────────

class TestMarksLocking:
    @pytest.fixture
    def exam(self, school):
        return f.ExamFactory(section=school.section, subject=school.subject, academic_year=school.year)

    def test_teacher_cannot_change_approved_marks(self, login, teacher, school, exam):
        m = f.MarkFactory(student=school.student, exam=exam, obtained_marks=50, status='approved')
        login(teacher).post(reverse('academics:marks_entry', args=[exam.pk]), {
            f'marks_{school.student.pk}': '99', 'action': 'draft'})
        m.refresh_from_db()
        assert m.obtained_marks == 50

    def test_admin_can_correct_approved_marks_and_status_stays_approved(self, login, admin, school, exam):
        m = f.MarkFactory(student=school.student, exam=exam, obtained_marks=50, status='approved')
        login(admin).post(reverse('academics:marks_entry', args=[exam.pk]), {
            f'marks_{school.student.pk}': '55', 'action': 'draft'})
        m.refresh_from_db()
        assert m.obtained_marks == 55 and m.status == 'approved'

    @pytest.mark.parametrize("raw, stored", [('150', 100), ('-10', 0), ('abc', None)])
    def test_marks_are_clamped_to_exam_range(self, login, teacher, school, exam, raw, stored):
        login(teacher).post(reverse('academics:marks_entry', args=[exam.pk]), {
            f'marks_{school.student.pk}': raw, 'action': 'draft'})
        m = Mark.objects.get(student=school.student, exam=exam)
        assert (m.obtained_marks if m.obtained_marks is None else int(m.obtained_marks)) == stored

    def test_inactive_students_are_not_listed(self, login, teacher, school, exam):
        school.expat.is_active = False
        school.expat.save()
        resp = login(teacher).get(reverse('academics:marks_entry', args=[exam.pk]))
        listed = [r['student'] for r in resp.context['rows']]
        assert school.student in listed and school.expat not in listed
