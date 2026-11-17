"""
Grading scales — the single source of truth for letters, marks /20 and GPA.

Decided by the school (2026-11-17):
  AMERICAN  A+ ≥90, A ≥85, B+ ≥80, B ≥75, C+ ≥70, C ≥65, D ≥60, F      → GPA 4.0
  BRITISH   A* ≥90, A ≥80, B ≥70, C ≥60, D ≥50, E ≥40, U               → overall average %
  FRENCH    mark out of 20 (= % ÷ 5) + mention                           → overall mark /20

A grade follows its division's curriculum; a GradeConfig.gpa_scale overrides it.
Pass / fail is NOT decided here — it follows GradeConfig.passing_marks.
"""
AMERICAN, BRITISH, FRENCH = 'AMERICAN', 'BRITISH', 'FRENCH'
ABSENT = 'AB'

_AMERICAN_BANDS = [(90, 'A+'), (85, 'A'), (80, 'B+'), (75, 'B'), (70, 'C+'), (65, 'C'), (60, 'D'), (0, 'F')]
_BRITISH_BANDS  = [(90, 'A*'), (80, 'A'), (70, 'B'), (60, 'C'), (50, 'D'), (40, 'E'), (0, 'U')]
_FRENCH_MENTIONS = [(16, 'Très bien'), (14, 'Bien'), (12, 'Assez bien'), (10, 'Passable'), (0, 'Insuffisant')]
_AMERICAN_GPA = {'A+': 4.0, 'A': 4.0, 'B+': 3.5, 'B': 3.0, 'C+': 2.5, 'C': 2.0, 'D': 1.0, 'F': 0.0, ABSENT: 0.0}


def scale_for_grade(grade):
    """Grading scale for a Grade (instance or pk)."""
    from academics.models import GradeConfig
    from core.models import Grade

    grade_id = getattr(grade, 'pk', grade)
    configured = GradeConfig.objects.filter(grade_id=grade_id).values_list('gpa_scale', flat=True).first()
    if configured:
        return configured
    if not hasattr(grade, 'division'):
        grade = Grade.objects.select_related('division').filter(pk=grade_id).first()
    curriculum = getattr(getattr(grade, 'division', None), 'curriculum_type', None)
    return curriculum if curriculum in (BRITISH, FRENCH) else AMERICAN


def _band(value, bands):
    for floor, name in bands:
        if value >= floor:
            return name
    return bands[-1][1]


def out_of_twenty(pct):
    return round(float(pct) / 5, 2)


def _fmt20(pct):
    return f"{round(float(pct) / 5, 1):g}/20"


def label(pct, scale):
    """Per-result label: 'A+' (American), 'A*' (British) or '14.5/20' (French). None → 'AB'."""
    if pct is None:
        return ABSENT
    if scale == BRITISH:
        return _band(pct, _BRITISH_BANDS)
    if scale == FRENCH:
        return _fmt20(pct)
    return _band(pct, _AMERICAN_BANDS)


def mention(pct):
    """French mention, decided on the exact mark /20 (not the rounded display)."""
    if pct is None:
        return ''
    return _band(out_of_twenty(pct), _FRENCH_MENTIONS)


def gpa_points(letter, scale):
    """4.0-scale points — American only; other curricula have no GPA."""
    if scale != AMERICAN:
        return None
    return _AMERICAN_GPA.get(letter, 0.0)


def overall(subject_pcts, scale):
    """
    Overall result for a report card from per-subject averages (None = absent → counts as 0,
    the same way an absent subject counts as 0 GPA points on the American scale).
    """
    if not subject_pcts:
        return {'overall_gpa': None, 'overall_pct': None, 'overall_label': None, 'overall_mention': ''}
    if scale == AMERICAN:
        pts = [gpa_points(label(p, AMERICAN), AMERICAN) for p in subject_pcts]
        return {'overall_gpa': round(sum(pts) / len(pts), 2), 'overall_pct': None,
                'overall_label': None, 'overall_mention': ''}
    avg = round(sum((p or 0) for p in subject_pcts) / len(subject_pcts), 1)
    return {'overall_gpa': None, 'overall_pct': avg, 'overall_label': label(avg, scale),
            'overall_mention': mention(avg) if scale == FRENCH else ''}
