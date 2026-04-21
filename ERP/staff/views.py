import csv
from datetime import date, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Sum
from django.utils import timezone

from accounts.decorators import role_required
from accounts.models import CustomUser
from attendance.models import StaffAttendance
from academics.models import Exam, Mark
from core.models import AcademicYear
from students.models import Student

from .models import StaffProfile, TeacherAssignment, VacationRequest, MOEApproval
from .forms import (
    StaffProfileForm, TeacherAssignmentForm,
    VacationRequestForm, VacationApprovalForm,
    MOEApprovalForm, StaffFilterForm,
)

_ADMIN      = ('SUPER_ADMIN', 'ADMIN')
_MANAGEMENT = ('SUPER_ADMIN', 'ADMIN', 'ACCOUNTANT')


# ──────────────────────────────────────────────────────────────────────────────
# STAFF DASHBOARD  (admin landing for this module)
# ──────────────────────────────────────────────────────────────────────────────

@login_required
@role_required(*_MANAGEMENT)
def staff_dashboard(request):
    today              = timezone.localdate()
    expiry_threshold   = today + timedelta(days=90)

    total_staff        = StaffProfile.objects.count()
    total_teachers     = StaffProfile.objects.filter(user__role='TEACHER').count()
    total_saudi        = StaffProfile.objects.filter(contract_type='SAUDI').count()
    total_foreign      = StaffProfile.objects.filter(contract_type='FOREIGN').count()
    pending_vacations  = VacationRequest.objects.filter(status='PENDING').count()
    iqama_expiring     = StaffProfile.objects.filter(
        contract_type='FOREIGN',
        iqama_expiry__isnull=False,
        iqama_expiry__lte=expiry_threshold,
    ).count()
    moe_expiring       = MOEApproval.objects.filter(
        status='APPROVED',
        expiry_date__isnull=False,
        expiry_date__lte=today + timedelta(days=60),
    ).count()

    recent_requests    = (VacationRequest.objects
                          .select_related('staff', 'approved_by')
                          .order_by('-created_at')[:6])

    dept_breakdown     = (StaffProfile.objects
                          .values('department')
                          .annotate(count=Count('id'))
                          .order_by('department'))

    return render(request, 'staff/dashboard.html', {
        'total_staff':      total_staff,
        'total_teachers':   total_teachers,
        'total_saudi':      total_saudi,
        'total_foreign':    total_foreign,
        'pending_vacations': pending_vacations,
        'iqama_expiring':   iqama_expiring,
        'moe_expiring':     moe_expiring,
        'recent_requests':  recent_requests,
        'dept_breakdown':   dept_breakdown,
    })


# ──────────────────────────────────────────────────────────────────────────────
# STAFF LIST
# ──────────────────────────────────────────────────────────────────────────────

@login_required
@role_required(*_MANAGEMENT)
def staff_list(request):
    form = StaffFilterForm(request.GET or None)
    qs   = StaffProfile.objects.select_related('user', 'division').order_by(
        'department', 'user__full_name')

    if form.is_valid():
        q         = form.cleaned_data.get('q', '').strip()
        dept      = form.cleaned_data.get('department')
        desig     = form.cleaned_data.get('designation')
        contract  = form.cleaned_data.get('contract_type')
        role      = form.cleaned_data.get('role')

        if q:
            qs = qs.filter(
                Q(user__full_name__icontains=q) |
                Q(employee_id__icontains=q) |
                Q(user__email__icontains=q)
            )
        if dept:
            qs = qs.filter(department=dept)
        if desig:
            qs = qs.filter(designation=desig)
        if contract:
            qs = qs.filter(contract_type=contract)
        if role:
            qs = qs.filter(user__role=role)

    return render(request, 'staff/staff_list.html', {
        'profiles': qs,
        'form':     form,
    })


# ──────────────────────────────────────────────────────────────────────────────
# STAFF PROFILE (detail view)
# ──────────────────────────────────────────────────────────────────────────────

@login_required
def staff_profile(request, pk):
    profile = get_object_or_404(
        StaffProfile.objects.select_related('user', 'division')
                            .prefetch_related('subjects_taught'),
        pk=pk,
    )

    # Only admin or the profile owner
    if request.user.role not in ('SUPER_ADMIN', 'ADMIN') and request.user != profile.user:
        messages.error(request, "Access denied.")
        return redirect('core:dashboard')

    today = timezone.localdate()
    assignments = TeacherAssignment.objects.filter(
        teacher=profile.user,
    ).select_related('subject', 'section', 'section__grade', 'academic_year').order_by(
        '-academic_year__start_date', 'section', 'subject')

    recent_vacations = VacationRequest.objects.filter(
        staff=profile.user).order_by('-created_at')[:5]

    moe_docs = MOEApproval.objects.filter(staff=profile.user).order_by('-created_at')

    attendance_qs = StaffAttendance.objects.filter(
        staff=profile.user, date__year=today.year, date__month=today.month)
    attendance_this_month = attendance_qs.count()
    absences_this_month   = attendance_qs.filter(status='A').count()

    return render(request, 'staff/staff_profile.html', {
        'profile':               profile,
        'assignments':           assignments,
        'recent_vacations':      recent_vacations,
        'moe_docs':              moe_docs,
        'attendance_this_month': attendance_this_month,
        'absences_this_month':   absences_this_month,
        'today':                 today,
    })


# ──────────────────────────────────────────────────────────────────────────────
# STAFF PROFILE CREATE / EDIT
# ──────────────────────────────────────────────────────────────────────────────

@login_required
@role_required(*_ADMIN)
def staff_form(request, pk=None):
    instance = get_object_or_404(StaffProfile, pk=pk) if pk else None
    form     = StaffProfileForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, "Staff profile saved.")
        return redirect('staff:profile', pk=form.instance.pk)
    return render(request, 'staff/staff_form.html', {
        'form':     form,
        'instance': instance,
    })


@login_required
@role_required(*_ADMIN)
def staff_delete(request, pk):
    profile = get_object_or_404(StaffProfile, pk=pk)
    if request.method == 'POST':
        name = profile.user.full_name
        profile.delete()
        messages.success(request, f"Profile for {name} deleted.")
        return redirect('staff:staff_list')
    return render(request, 'staff/confirm_delete.html', {
        'label':      profile.user.full_name,
        'back_url':   'staff:staff_list',
    })


# ──────────────────────────────────────────────────────────────────────────────
# VACATION REQUESTS
# ──────────────────────────────────────────────────────────────────────────────

@login_required
def vacation_list(request):
    is_admin = request.user.role in ('SUPER_ADMIN', 'ADMIN')

    if is_admin:
        qs = VacationRequest.objects.select_related('staff', 'approved_by').order_by('-created_at')
        status_filter = request.GET.get('status', '')
        if status_filter:
            qs = qs.filter(status=status_filter)
    else:
        qs            = VacationRequest.objects.filter(staff=request.user).order_by('-created_at')
        status_filter = ''

    return render(request, 'staff/vacation_list.html', {
        'requests':      qs,
        'status_filter': status_filter,
        'is_admin':      is_admin,
    })


@login_required
def vacation_form(request, pk=None):
    instance = get_object_or_404(VacationRequest, pk=pk) if pk else None

    # Permission check: only owner or admin can edit; only PENDING can be edited
    if instance:
        if instance.staff != request.user and request.user.role not in ('SUPER_ADMIN', 'ADMIN'):
            messages.error(request, "Access denied.")
            return redirect('staff:vacation_list')
        if instance.status != 'PENDING':
            messages.warning(request, "Only pending requests can be edited.")
            return redirect('staff:vacation_list')

    form = VacationRequestForm(request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        if not instance:
            obj.staff = request.user
        obj.save()
        messages.success(
            request,
            "Vacation request submitted." if not instance else "Request updated.",
        )
        return redirect('staff:vacation_list')

    return render(request, 'staff/vacation_form.html', {
        'form':     form,
        'instance': instance,
    })


@login_required
@role_required(*_ADMIN)
def vacation_approve(request, pk):
    vr   = get_object_or_404(VacationRequest.objects.select_related('staff'), pk=pk)
    form = VacationApprovalForm(request.POST or None)

    if form.is_valid():
        action        = form.cleaned_data['action']
        vr.status     = action
        vr.approved_by = request.user
        vr.approved_at = timezone.now()
        if action == 'REJECTED':
            vr.rejection_reason = form.cleaned_data.get('rejection_reason', '')
        vr.save()
        messages.success(request, f"Request {action.lower()} successfully.")
        return redirect('staff:vacation_list')

    return render(request, 'staff/vacation_approve.html', {'vr': vr, 'form': form})


# ──────────────────────────────────────────────────────────────────────────────
# MOE / REGULATORY APPROVALS
# ──────────────────────────────────────────────────────────────────────────────

@login_required
@role_required(*_ADMIN)
def moe_list(request):
    qs            = MOEApproval.objects.select_related('staff').order_by('-created_at')
    status_filter = request.GET.get('status', '')
    type_filter   = request.GET.get('type', '')
    q             = request.GET.get('q', '').strip()

    if status_filter:
        qs = qs.filter(status=status_filter)
    if type_filter:
        qs = qs.filter(approval_type=type_filter)
    if q:
        qs = qs.filter(staff__full_name__icontains=q)

    expire_threshold = timezone.localdate() + timedelta(days=60)
    expiring_soon    = MOEApproval.objects.filter(
        status='APPROVED', expiry_date__isnull=False,
        expiry_date__lte=expire_threshold,
    ).count()

    return render(request, 'staff/moe_list.html', {
        'approvals':      qs,
        'expiring_soon':  expiring_soon,
        'status_filter':  status_filter,
        'type_filter':    type_filter,
        'q':              q,
        'status_choices': MOEApproval.STATUS_CHOICES,
        'type_choices':   MOEApproval.APPROVAL_TYPE_CHOICES,
    })


@login_required
@role_required(*_ADMIN)
def moe_form(request, pk=None):
    instance = get_object_or_404(MOEApproval, pk=pk) if pk else None
    form     = MOEApprovalForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        if not instance:
            obj.created_by = request.user
        obj.save()
        messages.success(request, "MOE approval record saved.")
        return redirect('staff:moe_list')
    return render(request, 'staff/moe_form.html', {'form': form, 'instance': instance})


@login_required
@role_required(*_ADMIN)
def moe_delete(request, pk):
    doc = get_object_or_404(MOEApproval, pk=pk)
    if request.method == 'POST':
        doc.delete()
        messages.success(request, "Document deleted.")
        return redirect('staff:moe_list')
    return render(request, 'staff/confirm_delete.html', {
        'label':    f"{doc.get_approval_type_display()} — {doc.staff.full_name}",
        'back_url': 'staff:moe_list',
    })


# ──────────────────────────────────────────────────────────────────────────────
# TEACHER ASSIGNMENTS
# ──────────────────────────────────────────────────────────────────────────────

@login_required
@role_required(*_ADMIN)
def teacher_assignment_list(request):
    current_year  = AcademicYear.objects.filter(is_current=True).first()
    year_id       = request.GET.get('year')
    selected_year = (AcademicYear.objects.filter(pk=year_id).first()
                     if year_id else current_year)

    qs = TeacherAssignment.objects.select_related(
        'teacher', 'subject', 'section', 'section__grade', 'academic_year',
    ).order_by('teacher__full_name', 'section__grade', 'section', 'subject')

    if selected_year:
        qs = qs.filter(academic_year=selected_year)

    return render(request, 'staff/teacher_assignment_list.html', {
        'assignments':   qs,
        'years':         AcademicYear.objects.all(),
        'selected_year': selected_year,
    })


@login_required
@role_required(*_ADMIN)
def teacher_assignment_form(request, pk=None):
    instance = get_object_or_404(TeacherAssignment, pk=pk) if pk else None
    form     = TeacherAssignmentForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, "Teacher assignment saved.")
        return redirect('staff:teacher_assignment_list')
    return render(request, 'staff/teacher_assignment_form.html', {
        'form': form, 'instance': instance,
    })


@login_required
@role_required(*_ADMIN)
def teacher_assignment_delete(request, pk):
    obj = get_object_or_404(TeacherAssignment, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Assignment removed.")
        return redirect('staff:teacher_assignment_list')
    return render(request, 'staff/confirm_delete.html', {
        'label':    str(obj),
        'back_url': 'staff:teacher_assignment_list',
    })


# ──────────────────────────────────────────────────────────────────────────────
# TEACHER DASHBOARD
# ──────────────────────────────────────────────────────────────────────────────

@login_required
@role_required('TEACHER')
def teacher_dashboard(request):
    user         = request.user
    today        = timezone.localdate()
    current_year = AcademicYear.objects.filter(is_current=True).first()

    # My class assignments this year
    assignments = TeacherAssignment.objects.filter(
        teacher=user,
        academic_year=current_year,
    ).select_related(
        'subject', 'section', 'section__grade',
    ).order_by('section__grade', 'section', 'subject')

    my_section_ids = list(assignments.values_list('section_id', flat=True))
    my_subject_ids = list(assignments.values_list('subject_id', flat=True))

    # Pending exams = exams for my sections+subjects with no marks entered yet
    pending_exams = (Exam.objects
                     .filter(
                         section_id__in=my_section_ids,
                         subject_id__in=my_subject_ids,
                         academic_year=current_year,
                     )
                     .exclude(marks__isnull=False)
                     .select_related('subject', 'section', 'exam_type')
                     .order_by('date'))[:10]

    # My vacation requests
    my_vacations = VacationRequest.objects.filter(staff=user).order_by('-created_at')[:5]

    # Staff attendance this month
    attn_qs       = StaffAttendance.objects.filter(
        staff=user, date__year=today.year, date__month=today.month)
    present_days  = attn_qs.filter(status='P').count()
    absent_days   = attn_qs.filter(status='A').count()
    recent_attn   = attn_qs.order_by('-date')[:7]

    # Total students I teach
    students_count = Student.objects.filter(
        section_id__in=my_section_ids, is_active=True).distinct().count()

    # My profile (if exists)
    try:
        my_profile = user.staff_profile
    except StaffProfile.DoesNotExist:
        my_profile = None

    return render(request, 'staff/teacher_dashboard.html', {
        'assignments':    assignments,
        'pending_exams':  pending_exams,
        'my_vacations':   my_vacations,
        'present_days':   present_days,
        'absent_days':    absent_days,
        'recent_attn':    recent_attn,
        'students_count': students_count,
        'current_year':   current_year,
        'today':          today,
        'my_profile':     my_profile,
    })


# ──────────────────────────────────────────────────────────────────────────────
# STAFF ATTENDANCE VIEW  (read-only daily roster)
# ──────────────────────────────────────────────────────────────────────────────

@login_required
@role_required(*_ADMIN)
def staff_attendance_view(request):
    today    = timezone.localdate()
    date_str = request.GET.get('date', str(today))
    try:
        selected_date = date.fromisoformat(date_str)
    except ValueError:
        selected_date = today

    all_staff = (CustomUser.objects
                 .exclude(role='PARENT')
                 .filter(is_active=True)
                 .order_by('full_name'))

    attendance_map = {
        a.staff_id: a
        for a in StaffAttendance.objects.filter(date=selected_date).select_related('staff')
    }

    staff_with_attendance = []
    for member in all_staff:
        att = attendance_map.get(member.pk)
        staff_with_attendance.append({
            'user':       member,
            'attendance': att,
            'status':     att.status if att else None,
        })

    present = sum(1 for s in staff_with_attendance if s['status'] == 'P')
    late    = sum(1 for s in staff_with_attendance if s['status'] == 'L')
    absent  = sum(1 for s in staff_with_attendance if s['status'] == 'A')

    return render(request, 'staff/staff_attendance.html', {
        'staff_list':    staff_with_attendance,
        'selected_date': selected_date,
        'present':       present,
        'late':          late,
        'absent':        absent,
        'total':         len(staff_with_attendance),
        'prev_date':     selected_date - timedelta(days=1),
        'next_date':     min(selected_date + timedelta(days=1), today),
    })
