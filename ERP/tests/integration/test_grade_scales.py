"""
Report cards, results pages and the Noor export show each division's own scale.
"""
import csv
import io
from decimal import Decimal as D

import pytest
from django.urls import reverse

from academics.views import _compute_report_data
from core.models import Division
from tests import factories as f

pytestmark = pytest.mark.django_db


@pytest.fixture
def make_class(db):
    """Build a class in a given curriculum with one student and two approved subject marks."""
    def _make(curriculum, scores=(92, 55)):
        year = f.AcademicYearFactory(is_current=True)
        div = f.DivisionFactory(name=f'{curriculum} Division', curriculum_type=curriculum)
        grade = f.GradeFactory(division=div)
        section = f.SectionFactory(grade=grade)
        student = f.StudentFactory(division=div, grade=grade, section=section, academic_year=year)
        for i, score in enumerate(scores):
            subj = f.SubjectFactory(name=f'Subject {curriculum} {i}', grade=grade, division=div)
            exam = f.ExamFactory(section=section, subject=subj, academic_year=year, term='T1', total_marks=100)
            f.MarkFactory(student=student, exam=exam, obtained_marks=D(str(score)), status='approved')
        return student, section, year
    return _make


class TestReportCardData:
    def test_american_keeps_gpa(self, make_class):
        student, _, year = make_class(Division.AMERICAN)
        data = _compute_report_data(student, year, 'T1')
        assert data['scale'] == 'AMERICAN'
        assert sorted(r['letter'] for r in data['subjects']) == ['A+', 'F']
        assert data['overall_gpa'] == 2.0                       # (4.0 + 0.0) / 2

    def test_british_uses_a_star_to_u_and_overall_average(self, make_class):
        student, _, year = make_class(Division.BRITISH)
        data = _compute_report_data(student, year, 'T1')
        assert data['scale'] == 'BRITISH'
        assert sorted(r['letter'] for r in data['subjects']) == ['A*', 'D']
        assert data['overall_gpa'] is None
        assert data['overall_pct'] == 73.5 and data['overall_label'] == 'B'

    def test_french_uses_marks_out_of_20_and_mention(self, make_class):
        student, _, year = make_class(Division.FRENCH, scores=(70, 55))
        data = _compute_report_data(student, year, 'T1')
        assert data['scale'] == 'FRENCH'
        assert sorted(r['letter'] for r in data['subjects']) == ['11/20', '14/20']
        assert {r['mention'] for r in data['subjects']} == {'Bien', 'Passable'}
        assert data['overall_label'] == '12.5/20' and data['overall_mention'] == 'Assez bien'

    def test_pass_fail_still_follows_pass_mark(self, make_class):
        student, _, year = make_class(Division.BRITISH, scores=(92, 55))
        assert _compute_report_data(student, year, 'T1')['passed'] is False   # 55 < default 60


class TestPagesRender:
    @pytest.mark.parametrize("curriculum, expect", [
        (Division.AMERICAN, ['A+', 'GPA']), (Division.BRITISH, ['A*', '73.5']),
        (Division.FRENCH, ['/20', 'Assez bien']),
    ])
    def test_report_card_page(self, login, admin, make_class, curriculum, expect):
        scores = (70, 55) if curriculum == Division.FRENCH else (92, 55)
        student, section, year = make_class(curriculum, scores)
        html = login(admin).get(reverse('academics:report_card', args=[student.pk]),
                                {'section': section.pk, 'academic_year': year.pk, 'term': 'T1'}).content.decode()
        for text in expect:
            assert text in html, f"{text!r} missing on {curriculum} report card"

    @pytest.mark.parametrize("curriculum", [Division.BRITISH, Division.FRENCH])
    def test_print_and_bulk_report_cards_render(self, login, admin, make_class, curriculum):
        student, section, year = make_class(curriculum)
        client = login(admin)
        resp = client.get(reverse('academics:report_card_pdf', args=[student.pk]),
                          {'academic_year': year.pk, 'term': 'T1'})
        assert resp.status_code == 200 and resp['Content-Type'] == 'application/pdf'
        assert client.get(reverse('academics:bulk_report_cards'),
                          {'section': section.pk, 'academic_year': year.pk, 'term': 'T1'}).status_code == 200

    def test_marks_entry_page_uses_british_scale(self, login, admin, make_class):
        student, section, year = make_class(Division.BRITISH)
        exam = student.marks.first().exam
        html = login(admin).get(reverse('academics:marks_entry', args=[exam.pk])).content.decode()
        assert 'A*' in html
        import re
        assert re.search(r'const GRADE_SCALE\s*=\s*"BRITISH"', html)
        assert re.search(r'const PASSING_MARKS\s*=\s*60;', html)


class TestNoorExport:
    def _rows(self, client, section, year):
        resp = client.get(reverse('academics:noor_export'), {'section': section.pk, 'year': year.pk, 'term': 'T1'})
        return list(csv.reader(io.StringIO(resp.content.decode('utf-8-sig'))))

    def test_british_section(self, login, admin, make_class):
        student, section, year = make_class(Division.BRITISH)
        rows = self._rows(login(admin), section, year)
        assert rows[0][-2] == 'Overall Grade'
        row = next(r for r in rows if r[0] == student.student_id)
        assert {'A*', 'D'} <= set(row) and row[-2] == 'B'

    def test_american_section_unchanged(self, login, admin, make_class):
        student, section, year = make_class(Division.AMERICAN)
        rows = self._rows(login(admin), section, year)
        assert rows[0][-2] == 'Overall GPA'
        assert next(r for r in rows if r[0] == student.student_id)[-2] == '2.0'
