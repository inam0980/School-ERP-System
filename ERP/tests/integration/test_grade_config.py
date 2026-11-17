"""
GradeConfig.passing_marks — admins could set a per-grade passing percentage,
but every pass/fail decision ignored it and used a hard-coded 60 %.
"""
import csv
import io
from decimal import Decimal as D

import pytest
from django.urls import reverse

from academics.models import GradeConfig, Mark
from academics.views import _compute_report_data
from tests import factories as f

pytestmark = [pytest.mark.django_db, pytest.mark.regression]


@pytest.fixture
def exam(school):
    return f.ExamFactory(section=school.section, subject=school.subject,
                         academic_year=school.year, term='T1', total_marks=100)


def _mark(student, exam, score, status='approved'):
    return f.MarkFactory(student=student, exam=exam, obtained_marks=D(str(score)), status=status)


# ── Unit-level: the rule itself ──────────────────────────────────────────────

class TestPassingRule:
    def test_default_is_60_when_grade_has_no_config(self, school):
        assert GradeConfig.passing_for(school.grade) == 60

    def test_configured_value_is_used(self, school):
        GradeConfig.objects.create(grade=school.grade, passing_marks=50)
        assert GradeConfig.passing_for(school.grade) == 50
        assert GradeConfig.passing_for(school.grade.pk) == 50          # id works too

    @pytest.mark.parametrize("passing, score, passed", [
        (50, 55, True), (50, 49, False), (70, 65, False), (70, 70, True), (60, 60, True),
    ])
    def test_mark_is_passed_follows_grade_config(self, school, exam, passing, score, passed):
        GradeConfig.objects.create(grade=school.grade, passing_marks=passing)
        assert _mark(school.student, exam, score).is_passed() is passed

    def test_absent_never_passes(self, school, exam):
        GradeConfig.objects.create(grade=school.grade, passing_marks=1)
        m = f.MarkFactory(student=school.student, exam=exam, is_absent=True, obtained_marks=None)
        assert m.is_passed() is False


# ── Every screen / export that decides pass or fail ──────────────────────────

class TestPassFailEverywhere:
    def test_report_card_uses_config(self, school, exam):
        GradeConfig.objects.create(grade=school.grade, passing_marks=50)
        _mark(school.student, exam, 55)
        data = _compute_report_data(school.student, school.year, 'T1')
        assert data['subjects'][0]['passed'] is True
        assert data['passed'] is True

    def test_report_card_stricter_config(self, school, exam):
        GradeConfig.objects.create(grade=school.grade, passing_marks=70)
        _mark(school.student, exam, 65)
        assert _compute_report_data(school.student, school.year, 'T1')['passed'] is False

    def test_report_card_default_unchanged_without_config(self, school, exam):
        _mark(school.student, exam, 59)
        assert _compute_report_data(school.student, school.year, 'T1')['passed'] is False

    def test_exam_results_page_counts_with_config(self, login, admin, school, exam):
        GradeConfig.objects.create(grade=school.grade, passing_marks=50)
        _mark(school.student, exam, 55)
        _mark(school.expat, exam, 45)
        ctx = login(admin).get(reverse('academics:exam_results', args=[exam.pk])).context
        assert ctx['passed'] == 1 and ctx['failed'] == 1

    def test_noor_export_result_uses_config(self, login, admin, school, exam):
        """The Noor CSV is submitted to the Ministry — its Pass/Fail must match the school rule."""
        GradeConfig.objects.create(grade=school.grade, passing_marks=50)
        _mark(school.student, exam, 55)
        _mark(school.expat, exam, 45)
        resp = login(admin).get(reverse('academics:noor_export'),
                                {'section': school.section.pk, 'year': school.year.pk, 'term': 'T1'})
        rows = list(csv.reader(io.StringIO(resp.content.decode('utf-8-sig'))))
        result = {r[0]: r[-1] for r in rows[1:]}
        assert result[school.student.student_id] == 'Pass'
        assert result[school.expat.student_id] == 'Fail'

    def test_noor_export_default_unchanged_without_config(self, login, admin, school, exam):
        _mark(school.student, exam, 59)
        resp = login(admin).get(reverse('academics:noor_export'),
                                {'section': school.section.pk, 'year': school.year.pk, 'term': 'T1'})
        rows = list(csv.reader(io.StringIO(resp.content.decode('utf-8-sig'))))
        assert {r[0]: r[-1] for r in rows[1:]}[school.student.student_id] == 'Fail'
