import json

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.cache import cache

from accounts.decorators import role_required
from core.models import AcademicYear, Section, Grade
from students.models import Student

from .analytics import (
    compute_attendance_risk, attendance_risk_summary,
    compute_student_grade_trends, compute_section_performance,
    compute_fee_default_risk,
    generate_performance_summary,
    validate_noor_export,
    RISK_HIGH, RISK_MEDIUM,
)

_ADMIN = ('SUPER_ADMIN', 'ADMIN')
_STAFF = ('SUPER_ADMIN', 'ADMIN', 'TEACHER', 'ACCOUNTANT', 'STAFF')
_MANAGEMENT = ('SUPER_ADMIN', 'ADMIN', 'ACCOUNTANT')

_CACHE_TTL = 1800  # 30 minutes


# ──────────────────────────────────────────────────────────────────────────────
# AI HUB DASHBOARD
# ──────────────────────────────────────────────────────────────────────────────

@login_required
@role_required(*_MANAGEMENT)
def ai_dashboard(request):
    current_year = AcademicYear.objects.filter(is_current=True).first()
    year_pk      = current_year.pk if current_year else 'none'
    cache_key    = f'ai_dashboard_stats_{year_pk}'

    stats = cache.get(cache_key)
    if stats is None:
        risk_list     = compute_attendance_risk(academic_year=current_year)
        attn_summary  = attendance_risk_summary(risk_list)

        grade_list    = compute_student_grade_trends(academic_year=current_year)
        failing_count = sum(1 for g in grade_list if g['failing_subjects'])

        fee_list      = compute_fee_default_risk(academic_year=current_year)
        fee_high      = sum(1 for f in fee_list if f['risk'] == RISK_HIGH)

        noor_result   = validate_noor_export(academic_year=current_year)

        stats = {
            'attn_summary':  attn_summary,
            'failing_count': failing_count,
            'fee_high':      fee_high,
            'noor_errors':   noor_result['error_count'],
            'noor_total':    noor_result['total'],
        }
        cache.set(cache_key, stats, _CACHE_TTL)

    return render(request, 'ai_features/dashboard.html', {
        'current_year':   current_year,
        **stats,
    })


# ──────────────────────────────────────────────────────────────────────────────
# 1. ATTENDANCE RISK
# ──────────────────────────────────────────────────────────────────────────────

@login_required
@role_required(*_STAFF)
def attendance_risk(request):
    current_year = AcademicYear.objects.filter(is_current=True).first()
    years        = AcademicYear.objects.all()
    grades       = Grade.objects.all()
    sections     = Section.objects.all().select_related('grade')

    year_id    = request.GET.get('year')
    grade_id   = request.GET.get('grade')
    section_id = request.GET.get('section')
    risk_filter = request.GET.get('risk', '')

    selected_year    = AcademicYear.objects.filter(pk=year_id).first() if year_id else current_year
    selected_grade   = Grade.objects.filter(pk=grade_id).first() if grade_id else None
    selected_section = Section.objects.filter(pk=section_id).first() if section_id else None

    risk_list = compute_attendance_risk(
        academic_year=selected_year,
        section=selected_section,
        grade=selected_grade,
    )

    if risk_filter:
        risk_list = [r for r in risk_list if r['risk'] == risk_filter]

    summary = attendance_risk_summary(risk_list)

    return render(request, 'ai_features/attendance_risk.html', {
        'risk_list':        risk_list,
        'summary':          summary,
        'years':            years,
        'grades':           grades,
        'sections':         sections,
        'selected_year':    selected_year,
        'selected_grade':   selected_grade,
        'selected_section': selected_section,
        'risk_filter':      risk_filter,
    })


# ──────────────────────────────────────────────────────────────────────────────
# 2. GRADE ANALYTICS
# ──────────────────────────────────────────────────────────────────────────────

@login_required
@role_required(*_STAFF)
def grade_analytics(request):
    current_year = AcademicYear.objects.filter(is_current=True).first()
    years        = AcademicYear.objects.all()
    grades       = Grade.objects.all()
    sections     = Section.objects.all().select_related('grade')

    year_id    = request.GET.get('year')
    grade_id   = request.GET.get('grade')
    section_id = request.GET.get('section')

    selected_year    = AcademicYear.objects.filter(pk=year_id).first() if year_id else current_year
    selected_grade   = Grade.objects.filter(pk=grade_id).first() if grade_id else None
    selected_section = Section.objects.filter(pk=section_id).first() if section_id else None

    student_trends   = compute_student_grade_trends(
        academic_year=selected_year,
        section=selected_section,
        grade=selected_grade,
    )

    section_perf = compute_section_performance(academic_year=selected_year)
    chart_json   = json.dumps({
        'labels': section_perf['labels'],
        'data':   section_perf['data'],
    })

    return render(request, 'ai_features/grade_analytics.html', {
        'student_trends':   student_trends,
        'section_perf':     section_perf['sections'],
        'chart_json':       chart_json,
        'years':            years,
        'grades':           grades,
        'sections':         sections,
        'selected_year':    selected_year,
        'selected_grade':   selected_grade,
        'selected_section': selected_section,
    })


# ──────────────────────────────────────────────────────────────────────────────
# 3. FEE DEFAULT PREDICTION
# ──────────────────────────────────────────────────────────────────────────────

@login_required
@role_required('SUPER_ADMIN', 'ADMIN', 'ACCOUNTANT')
def fee_default_risk(request):
    current_year = AcademicYear.objects.filter(is_current=True).first()
    years        = AcademicYear.objects.all()

    year_id      = request.GET.get('year')
    risk_filter  = request.GET.get('risk', '')
    selected_year = AcademicYear.objects.filter(pk=year_id).first() if year_id else current_year

    fee_list = compute_fee_default_risk(academic_year=selected_year)
    if risk_filter:
        fee_list = [f for f in fee_list if f['risk'] == risk_filter]

    high   = sum(1 for f in fee_list if f['risk'] == RISK_HIGH)
    medium = sum(1 for f in fee_list if f['risk'] == RISK_MEDIUM)

    return render(request, 'ai_features/fee_default_risk.html', {
        'fee_list':     fee_list,
        'years':        years,
        'selected_year': selected_year,
        'risk_filter':  risk_filter,
        'high_count':   high,
        'medium_count': medium,
    })


# ──────────────────────────────────────────────────────────────────────────────
# 4. SMART PERFORMANCE SUMMARY
# ──────────────────────────────────────────────────────────────────────────────

@login_required
@role_required(*_STAFF)
def performance_summary(request, student_pk):
    student      = get_object_or_404(Student, pk=student_pk)
    current_year = AcademicYear.objects.filter(is_current=True).first()

    year_id      = request.GET.get('year')
    selected_year = AcademicYear.objects.filter(pk=year_id).first() if year_id else current_year

    summary_text = generate_performance_summary(student, academic_year=selected_year)

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'summary': summary_text})

    years = AcademicYear.objects.all()
    return render(request, 'ai_features/performance_summary.html', {
        'student':       student,
        'summary_text':  summary_text,
        'years':         years,
        'selected_year': selected_year,
    })


# ──────────────────────────────────────────────────────────────────────────────
# 5. NOOR CSV VALIDATION
# ──────────────────────────────────────────────────────────────────────────────

@login_required
@role_required(*_ADMIN)
def noor_validation(request):
    current_year  = AcademicYear.objects.filter(is_current=True).first()
    years         = AcademicYear.objects.all()
    year_id       = request.GET.get('year')
    selected_year = AcademicYear.objects.filter(pk=year_id).first() if year_id else current_year

    result = validate_noor_export(academic_year=selected_year)

    return render(request, 'ai_features/noor_validation.html', {
        'result':        result,
        'years':         years,
        'selected_year': selected_year,
    })

