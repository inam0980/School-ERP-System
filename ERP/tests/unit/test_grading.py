"""
Grading scales per curriculum (decided by the school, 2026-11-17):

AMERICAN  A+ ≥90, A ≥85, B+ ≥80, B ≥75, C+ ≥70, C ≥65, D ≥60, F  — GPA 4.0
BRITISH   A* ≥90, A ≥80, B ≥70, C ≥60, D ≥50, E ≥40, U
FRENCH    mark out of 20 (= % ÷ 5); mention Très bien ≥16, Bien ≥14,
          Assez bien ≥12, Passable ≥10, Insuffisant

A grade uses its division's curriculum; a GradeConfig.gpa_scale overrides it.
"""
from decimal import Decimal as D

import pytest

from academics import grading
from academics.models import GradeConfig, Mark
from academics.templatetags.grading_tags import grade_css
from core.models import Division
from tests import factories as f

pytestmark = pytest.mark.django_db


def _grade(curriculum):
    div = f.DivisionFactory(name=f'{curriculum} DIV', curriculum_type=curriculum)
    return f.GradeFactory(division=div)


class TestScaleForGrade:
    @pytest.mark.parametrize("curriculum, scale", [
        (Division.AMERICAN, 'AMERICAN'), (Division.BRITISH, 'BRITISH'),
        (Division.FRENCH, 'FRENCH'), (Division.HOME_STUDY, 'AMERICAN'),
    ])
    def test_follows_division_curriculum(self, curriculum, scale):
        assert grading.scale_for_grade(_grade(curriculum)) == scale

    def test_grade_config_overrides_curriculum(self):
        g = _grade(Division.BRITISH)
        GradeConfig.objects.create(grade=g, gpa_scale='FRENCH')
        assert grading.scale_for_grade(g) == 'FRENCH'

    def test_accepts_grade_id(self):
        g = _grade(Division.FRENCH)
        assert grading.scale_for_grade(g.pk) == 'FRENCH'


class TestLabels:
    @pytest.mark.parametrize("pct, label", [
        (100, 'A+'), (90, 'A+'), (85, 'A'), (80, 'B+'), (75, 'B'), (70, 'C+'), (65, 'C'), (60, 'D'), (59.9, 'F'),
    ])
    def test_american_unchanged(self, pct, label):
        assert grading.label(pct, 'AMERICAN') == label

    @pytest.mark.parametrize("pct, label", [
        (100, 'A*'), (90, 'A*'), (89.9, 'A'), (80, 'A'), (70, 'B'), (60, 'C'), (50, 'D'), (40, 'E'), (39.9, 'U'), (0, 'U'),
    ])
    def test_british(self, pct, label):
        assert grading.label(pct, 'BRITISH') == label

    @pytest.mark.parametrize("pct, label, mention", [
        (100, '20/20', 'Très bien'), (80, '16/20', 'Très bien'), (79, '15.8/20', 'Bien'),
        (70, '14/20', 'Bien'), (60, '12/20', 'Assez bien'), (50, '10/20', 'Passable'),
        (49.9, '10/20', 'Insuffisant'),     # 9.98 shows as 10/20 but the mention uses the exact mark
        (45, '9/20', 'Insuffisant'), (0, '0/20', 'Insuffisant'),
    ])
    def test_french(self, pct, label, mention):
        assert grading.label(pct, 'FRENCH') == label
        assert grading.mention(pct) == mention

    @pytest.mark.parametrize("scale", ['AMERICAN', 'BRITISH', 'FRENCH'])
    def test_absent(self, scale):
        assert grading.label(None, scale) == 'AB'

    def test_gpa_points_only_for_american(self):
        assert grading.gpa_points('A+', 'AMERICAN') == 4.0
        assert grading.gpa_points('AB', 'AMERICAN') == 0.0
        assert grading.gpa_points('A*', 'BRITISH') is None
        assert grading.gpa_points('15/20', 'FRENCH') is None


class TestMarkUsesScale:
    def _mark(self, curriculum, score):
        g = _grade(curriculum)
        exam = f.ExamFactory(section=f.SectionFactory(grade=g), total_marks=100)
        return Mark(exam=exam, obtained_marks=D(str(score)))

    def test_british_mark(self):
        m = self._mark(Division.BRITISH, 92)
        assert m.get_letter_grade() == 'A*' and m.get_gpa_points() is None

    def test_french_mark(self):
        assert self._mark(Division.FRENCH, 72).get_letter_grade() == '14.4/20'

    def test_american_mark(self):
        m = self._mark(Division.AMERICAN, 92)
        assert m.get_letter_grade() == 'A+' and m.get_gpa_points() == 4.0


class TestGradeCss:
    @pytest.mark.parametrize("label, colour", [
        ('A+', 'green'), ('A*', 'green'), ('A', 'green'), ('B+', 'blue'), ('B', 'blue'),
        ('C+', 'yellow'), ('C', 'yellow'), ('D', 'orange'), ('E', 'orange'),
        ('F', 'red'), ('U', 'red'), ('AB', 'slate'),
        ('17/20', 'green'), ('14/20', 'green'), ('12.5/20', 'blue'), ('10/20', 'yellow'), ('9.5/20', 'red'),
    ])
    def test_colour_tiers(self, label, colour):
        assert f'bg-{colour}-100' in grade_css(label)
