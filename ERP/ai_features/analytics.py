"""
ai_features/analytics.py
Pure-Python / scikit-learn analytics engine.
All functions are stateless and return plain dicts/lists so
views can easily pass them to templates.
"""
from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal

from django.db.models import Avg, Count, Q, Sum
from django.utils import timezone


# ── helpers ───────────────────────────────────────────────────────────────────

def _pct(part: int, total: int) -> float:
    return round(part / total * 100, 1) if total else 0.0


# ══════════════════════════════════════════════════════════════════════════════
# 1.  ATTENDANCE RISK
# ══════════════════════════════════════════════════════════════════════════════

RISK_HIGH   = "HIGH"
RISK_MEDIUM = "MEDIUM"
RISK_LOW    = "LOW"


def _attendance_risk_label(pct: float) -> str:
    if pct < 70:
        return RISK_HIGH
    if pct < 80:
        return RISK_MEDIUM
    return RISK_LOW


def compute_attendance_risk(academic_year=None, section=None, grade=None):
    """
    Returns a list of dicts, one per active student, ordered by risk (worst first).
    Each dict: {student, total, present, late, pct, risk}
    Uses pure threshold logic (no sklearn needed for this).
    """
    from attendance.models import Attendance
    from students.models import Student

    qs = Student.objects.filter(is_active=True).select_related(
        'section', 'grade', 'division', 'academic_year'
    )
    if academic_year:
        qs = qs.filter(academic_year=academic_year)
    if section:
        qs = qs.filter(section=section)
    if grade:
        qs = qs.filter(grade=grade)

    results = []
    for student in qs:
        attn = Attendance.objects.filter(student=student)
        if academic_year:
            attn = attn.filter(
                date__gte=academic_year.start_date,
                date__lte=min(academic_year.end_date, timezone.localdate()),
            )
        total   = attn.count()
        present = attn.filter(status__in=['P', 'L']).count()  # late counts as present
        pct     = _pct(present, total)
        results.append({
            'student': student,
            'total':   total,
            'present': present,
            'pct':     pct,
            'risk':    _attendance_risk_label(pct) if total >= 5 else RISK_LOW,
        })

    results.sort(key=lambda x: x['pct'])
    return results


def attendance_risk_summary(risk_list: list) -> dict:
    high   = sum(1 for r in risk_list if r['risk'] == RISK_HIGH)
    medium = sum(1 for r in risk_list if r['risk'] == RISK_MEDIUM)
    low    = sum(1 for r in risk_list if r['risk'] == RISK_LOW)
    return {'high': high, 'medium': medium, 'low': low, 'total': len(risk_list)}


# ══════════════════════════════════════════════════════════════════════════════
# 2.  GRADE ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════

TREND_IMPROVING = "IMPROVING"
TREND_DECLINING = "DECLINING"
TREND_STABLE    = "STABLE"
TREND_NO_DATA   = "NO_DATA"


def _trend_label(scores: list[float]) -> str:
    """Given a list of percentage scores (oldest first), return a trend label."""
    if len(scores) < 2:
        return TREND_NO_DATA
    diffs = [scores[i] - scores[i - 1] for i in range(1, len(scores))]
    avg_diff = sum(diffs) / len(diffs)
    if avg_diff >= 3:
        return TREND_IMPROVING
    if avg_diff <= -3:
        return TREND_DECLINING
    return TREND_STABLE


def compute_student_grade_trends(academic_year=None, section=None, grade=None):
    """
    Returns list of dicts per student:
    {student, avg_pct, trend, subject_breakdown: [{subject, avg_pct, trend}], failing_subjects}
    """
    from academics.models import Mark
    from students.models import Student

    qs = Student.objects.filter(is_active=True).select_related(
        'section', 'grade', 'division'
    ).prefetch_related('marks__exam__subject', 'marks__exam__exam_type')

    if academic_year:
        qs = qs.filter(academic_year=academic_year)
    if section:
        qs = qs.filter(section=section)
    if grade:
        qs = qs.filter(grade=grade)

    results = []
    for student in qs:
        marks = student.marks.filter(
            is_absent=False,
            obtained_marks__isnull=False,
            status='approved',
        )
        if academic_year:
            marks = marks.filter(exam__academic_year=academic_year)

        # Group by subject
        subject_data = {}
        for mark in marks.order_by('exam__date'):
            subj = mark.exam.subject
            pct  = mark.get_percentage()
            if pct is None:
                continue
            if subj.pk not in subject_data:
                subject_data[subj.pk] = {'subject': subj, 'scores': []}
            subject_data[subj.pk]['scores'].append(pct)

        subject_breakdown = []
        all_scores = []
        failing_subjects = []

        for subj_data in subject_data.values():
            scores = subj_data['scores']
            avg    = round(sum(scores) / len(scores), 1) if scores else 0
            trend  = _trend_label(scores)
            subject_breakdown.append({
                'subject': subj_data['subject'],
                'avg_pct': avg,
                'trend':   trend,
                'scores':  scores,
            })
            all_scores.extend(scores)
            if avg < 60:
                failing_subjects.append(subj_data['subject'].name)

        overall_avg = round(sum(all_scores) / len(all_scores), 1) if all_scores else 0
        overall_trend = _trend_label(all_scores[-6:]) if len(all_scores) >= 2 else TREND_NO_DATA

        results.append({
            'student':           student,
            'avg_pct':           overall_avg,
            'trend':             overall_trend,
            'subject_breakdown': sorted(subject_breakdown, key=lambda x: x['avg_pct']),
            'failing_subjects':  failing_subjects,
        })

    results.sort(key=lambda x: x['avg_pct'])
    return results


def compute_section_performance(academic_year=None):
    """
    Section-level avg performance for Chart.js.
    Returns: {labels: [...], data: [...], section_objs: [...]}
    """
    from academics.models import Mark
    from core.models import Section

    sections = Section.objects.all().select_related('grade', 'division')
    labels, data_points, section_objs = [], [], []

    for sec in sections:
        marks = Mark.objects.filter(
            exam__section=sec,
            is_absent=False,
            obtained_marks__isnull=False,
            status='approved',
        )
        if academic_year:
            marks = marks.filter(exam__academic_year=academic_year)

        if not marks.exists():
            continue

        pcts = [m.get_percentage() for m in marks if m.get_percentage() is not None]
        if not pcts:
            continue
        avg = round(sum(pcts) / len(pcts), 1)
        labels.append(f"{sec.grade.name} — {sec.name}")
        data_points.append(avg)
        section_objs.append({'section': sec, 'avg_pct': avg, 'count': len(pcts)})

    return {'labels': labels, 'data': data_points, 'sections': section_objs}


# ══════════════════════════════════════════════════════════════════════════════
# 3.  FEE DEFAULT PREDICTION
# ══════════════════════════════════════════════════════════════════════════════

def compute_fee_default_risk(academic_year=None):
    """
    Returns list of at-risk students for fee default.
    Simple rule-based: students with ≥1 OVERDUE fees or balance > 0 past due_date.
    Each item: {student, overdue_count, total_balance, risk}
    """
    from fees.models import StudentFee
    from students.models import Student

    today = timezone.localdate()
    qs = StudentFee.objects.select_related(
        'student', 'fee_structure__fee_type'
    ).filter(status__in=['OVERDUE', 'UNPAID', 'PARTIAL'])

    if academic_year:
        qs = qs.filter(fee_structure__academic_year=academic_year)

    # Group by student
    student_map: dict = {}
    for sf in qs:
        sid = sf.student_id
        if sid not in student_map:
            student_map[sid] = {
                'student':       sf.student,
                'overdue_count': 0,
                'total_balance': Decimal('0.00'),
                'days_overdue':  0,
            }
        entry = student_map[sid]
        balance = sf.balance
        if balance > 0:
            entry['total_balance'] += balance
        if sf.status == 'OVERDUE' or (sf.due_date < today and balance > 0):
            entry['overdue_count'] += 1
            days = (today - sf.due_date).days
            if days > entry['days_overdue']:
                entry['days_overdue'] = days

    results = []
    for entry in student_map.values():
        # Risk scoring
        score = entry['overdue_count'] * 2 + min(entry['days_overdue'] // 30, 3)
        entry['risk'] = RISK_HIGH if score >= 4 else (RISK_MEDIUM if score >= 2 else RISK_LOW)
        results.append(entry)

    results.sort(key=lambda x: (-x['overdue_count'], -float(x['total_balance'])))
    return results


# ══════════════════════════════════════════════════════════════════════════════
# 4.  SMART PERFORMANCE SUMMARY (template-based NLG)
# ══════════════════════════════════════════════════════════════════════════════

def generate_performance_summary(student, academic_year=None) -> str:
    """
    Generates a natural language performance paragraph for a student.
    Uses template-based approach; if OPENAI_API_KEY is set in settings,
    it calls GPT-4o-mini instead.
    """
    from academics.models import Mark
    from attendance.models import Attendance
    from django.conf import settings as django_settings

    # ── Attendance ────────────────────────────────────────────────────
    attn_qs = Attendance.objects.filter(student=student)
    if academic_year:
        attn_qs = attn_qs.filter(
            date__gte=academic_year.start_date,
            date__lte=min(academic_year.end_date, timezone.localdate()),
        )
    total_days  = attn_qs.count()
    present_days = attn_qs.filter(status__in=['P', 'L']).count()
    attn_pct    = _pct(present_days, total_days)

    # ── Marks ────────────────────────────────────────────────────────
    marks_qs = student.marks.filter(is_absent=False, obtained_marks__isnull=False, status='approved')
    if academic_year:
        marks_qs = marks_qs.filter(exam__academic_year=academic_year)

    pcts = [m.get_percentage() for m in marks_qs if m.get_percentage() is not None]
    avg_pct  = round(sum(pcts) / len(pcts), 1) if pcts else None
    trend    = _trend_label(pcts[-6:]) if len(pcts) >= 2 else TREND_NO_DATA

    # ── Try OpenAI if configured ───────────────────────────────────────
    openai_key = getattr(django_settings, 'OPENAI_API_KEY', '').strip()
    if openai_key and avg_pct is not None:
        try:
            return _generate_with_openai(
                student.full_name, attn_pct, avg_pct, trend, openai_key
            )
        except Exception:
            pass  # fall through to template

    # ── Template-based fallback ────────────────────────────────────────
    return _template_summary(student.full_name, attn_pct, avg_pct, trend, total_days)


def _template_summary(name, attn_pct, avg_pct, trend, total_days) -> str:
    if avg_pct is None:
        return (
            f"{name} has {total_days} attendance records this year. "
            "No approved mark data is available yet to generate a full academic summary."
        )

    grade_word = (
        "excellent" if avg_pct >= 85 else
        "good"      if avg_pct >= 70 else
        "average"   if avg_pct >= 60 else "below average"
    )

    attn_word = (
        "excellent" if attn_pct >= 90 else
        "satisfactory" if attn_pct >= 75 else
        "concerning"
    )

    trend_phrase = {
        TREND_IMPROVING: "showing a positive upward trend",
        TREND_DECLINING: "showing a declining trend that requires intervention",
        TREND_STABLE:    "maintaining a consistent performance level",
        TREND_NO_DATA:   "with limited data for trend analysis",
    }[trend]

    attn_advice = (
        "" if attn_pct >= 75 else
        f" Attendance of {attn_pct}% is below the minimum requirement of 75% and needs immediate attention."
    )

    return (
        f"{name} has achieved an overall average of {avg_pct}% this academic year, "
        f"which is considered {grade_word}. The student's performance is {trend_phrase}. "
        f"Attendance stands at {attn_pct}% ({total_days} school days recorded), "
        f"which is {attn_word}.{attn_advice}"
    )


def _generate_with_openai(name, attn_pct, avg_pct, trend, api_key) -> str:
    import urllib.request, json as _json
    prompt = (
        f"Write a concise, professional 2-sentence academic performance summary for "
        f"a student named {name}. Their overall grade average is {avg_pct}%, "
        f"attendance is {attn_pct}%, and performance trend is {trend.lower()}. "
        f"Keep it factual and suitable for a school report card."
    )
    payload = _json.dumps({
        "model": "gpt-4o-mini",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 120,
    }).encode()
    req = urllib.request.Request(
        "https://api.openai.com/v1/chat/completions",
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=10) as resp:
        result = _json.loads(resp.read())
    return result["choices"][0]["message"]["content"].strip()


# ══════════════════════════════════════════════════════════════════════════════
# 5.  NOOR CSV VALIDATION
# ══════════════════════════════════════════════════════════════════════════════

NOOR_REQUIRED_FIELDS = [
    ('student_id',    'Student ID'),
    ('full_name',     'Full Name (EN)'),
    ('arabic_name',   'Full Name (AR)'),
    ('dob',           'Date of Birth'),
    ('gender',        'Gender'),
    ('nationality',   'Nationality'),
    ('grade',         'Grade'),
    ('section',       'Section'),
    ('national_id',   'National ID'),
    ('guardian_phone','Guardian Phone'),
]


def validate_noor_export(academic_year=None):
    """
    Validates all active students for NOOR export completeness.
    Returns: {errors: [{student, missing_fields}], valid_count, error_count}
    """
    from students.models import Student

    qs = Student.objects.filter(is_active=True).select_related(
        'grade', 'section', 'division', 'academic_year'
    )
    if academic_year:
        qs = qs.filter(academic_year=academic_year)

    errors = []
    valid_count = 0

    for student in qs:
        missing = []
        for field_name, label in NOOR_REQUIRED_FIELDS:
            val = getattr(student, field_name, None)
            # FK fields: check if set
            if hasattr(val, 'pk'):
                if val.pk is None:
                    missing.append(label)
            elif val in (None, '', b''):
                missing.append(label)

        if missing:
            errors.append({'student': student, 'missing_fields': missing})
        else:
            valid_count += 1

    return {
        'errors':      errors,
        'valid_count': valid_count,
        'error_count': len(errors),
        'total':       valid_count + len(errors),
    }
