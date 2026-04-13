from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q

from accounts.decorators import role_required
from .models import AcademicYear, Division, Grade, Section, Subject
from .forms import AcademicYearForm, DivisionForm, GradeForm, SectionForm, SubjectForm

_ADMIN = ('SUPER_ADMIN', 'ADMIN')


# ────────────────────────── DASHBOARD ──────────────────────────

@login_required
def dashboard(request):
    from datetime import date
    stats = {}
    try:
        from students.models import Student
        stats['total_students'] = Student.objects.filter(is_active=True).count()
    except Exception:
        stats['total_students'] = '—'
    try:
        from attendance.models import Attendance
        today = date.today()
        total_active  = Student.objects.filter(is_active=True).count()
        present_today = Attendance.objects.filter(date=today, status__in=['P', 'L']).count()
        marked_today  = Attendance.objects.filter(date=today).count()
        stats['attendance_today'] = f"{round(present_today / total_active * 100)}%" if total_active else '—'
        stats['marked_today']     = marked_today
    except Exception:
        stats['attendance_today'] = '—'
    stats.setdefault('pending_fees', '—')
    stats.setdefault('total_staff', '—')
    return render(request, 'core/dashboard.html', {'stats': stats})


# ────────────────────────── ACADEMIC YEARS ──────────────────────────

@login_required
@role_required(*_ADMIN)
def academic_year_list(request):
    q  = request.GET.get('q', '')
    qs = AcademicYear.objects.all()
    if q:
        qs = qs.filter(name__icontains=q)
    return render(request, 'core/school_setup/academic_years.html', {'years': qs, 'q': q})


@login_required
@role_required(*_ADMIN)
def academic_year_add(request):
    form = AcademicYearForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Academic Year added successfully.")
        return redirect('core:academic_year_list')
    return render(request, 'core/school_setup/form.html', {
        'form': form, 'title': 'Add Academic Year', 'back_url': 'core:academic_year_list',
    })


@login_required
@role_required(*_ADMIN)
def academic_year_edit(request, pk):
    obj  = get_object_or_404(AcademicYear, pk=pk)
    form = AcademicYearForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Academic Year updated.")
        return redirect('core:academic_year_list')
    return render(request, 'core/school_setup/form.html', {
        'form': form, 'title': f'Edit: {obj}', 'back_url': 'core:academic_year_list',
    })


@login_required
@role_required(*_ADMIN)
def academic_year_delete(request, pk):
    obj = get_object_or_404(AcademicYear, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Academic Year deleted.")
        return redirect('core:academic_year_list')
    return render(request, 'core/school_setup/confirm_delete.html', {
        'obj': obj, 'back_url': 'core:academic_year_list',
    })


# ────────────────────────── DIVISIONS ──────────────────────────

@login_required
@role_required(*_ADMIN)
def division_list(request):
    divisions = Division.objects.all()
    return render(request, 'core/school_setup/divisions.html', {'divisions': divisions})


@login_required
@role_required(*_ADMIN)
def division_add(request):
    form = DivisionForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Division added.")
        return redirect('core:division_list')
    return render(request, 'core/school_setup/form.html', {
        'form': form, 'title': 'Add Division', 'back_url': 'core:division_list',
    })


@login_required
@role_required(*_ADMIN)
def division_edit(request, pk):
    obj  = get_object_or_404(Division, pk=pk)
    form = DivisionForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Division updated.")
        return redirect('core:division_list')
    return render(request, 'core/school_setup/form.html', {
        'form': form, 'title': f'Edit: {obj}', 'back_url': 'core:division_list',
    })


@login_required
@role_required(*_ADMIN)
def division_delete(request, pk):
    obj = get_object_or_404(Division, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Division deleted.")
        return redirect('core:division_list')
    return render(request, 'core/school_setup/confirm_delete.html', {
        'obj': obj, 'back_url': 'core:division_list',
    })


# ────────────────────────── GRADES ──────────────────────────

@login_required
@role_required(*_ADMIN)
def grade_list(request):
    q      = request.GET.get('q', '')
    div_id = request.GET.get('division', '')
    qs     = Grade.objects.select_related('division').all()
    if q:
        qs = qs.filter(name__icontains=q)
    if div_id:
        qs = qs.filter(division_id=div_id)
    return render(request, 'core/school_setup/grades.html', {
        'grades': qs, 'divisions': Division.objects.all(),
        'q': q, 'selected_div': div_id,
    })


@login_required
@role_required(*_ADMIN)
def grade_add(request):
    form = GradeForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Grade added.")
        return redirect('core:grade_list')
    return render(request, 'core/school_setup/form.html', {
        'form': form, 'title': 'Add Grade', 'back_url': 'core:grade_list',
    })


@login_required
@role_required(*_ADMIN)
def grade_edit(request, pk):
    obj  = get_object_or_404(Grade, pk=pk)
    form = GradeForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Grade updated.")
        return redirect('core:grade_list')
    return render(request, 'core/school_setup/form.html', {
        'form': form, 'title': f'Edit: {obj.name}', 'back_url': 'core:grade_list',
    })


@login_required
@role_required(*_ADMIN)
def grade_delete(request, pk):
    obj = get_object_or_404(Grade, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Grade deleted.")
        return redirect('core:grade_list')
    return render(request, 'core/school_setup/confirm_delete.html', {
        'obj': obj, 'back_url': 'core:grade_list',
    })


# ────────────────────────── SECTIONS ──────────────────────────

@login_required
@role_required(*_ADMIN)
def section_list(request):
    grade_id = request.GET.get('grade', '')
    qs       = Section.objects.select_related('grade__division', 'class_teacher').all()
    if grade_id:
        qs = qs.filter(grade_id=grade_id)
    return render(request, 'core/school_setup/sections.html', {
        'sections': qs,
        'grades':   Grade.objects.select_related('division').all(),
        'selected_grade': grade_id,
    })


@login_required
@role_required(*_ADMIN)
def section_add(request):
    form = SectionForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Section added.")
        return redirect('core:section_list')
    return render(request, 'core/school_setup/form.html', {
        'form': form, 'title': 'Add Section', 'back_url': 'core:section_list',
    })


@login_required
@role_required(*_ADMIN)
def section_edit(request, pk):
    obj  = get_object_or_404(Section, pk=pk)
    form = SectionForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Section updated.")
        return redirect('core:section_list')
    return render(request, 'core/school_setup/form.html', {
        'form': form, 'title': f'Edit: {obj}', 'back_url': 'core:section_list',
    })


@login_required
@role_required(*_ADMIN)
def section_delete(request, pk):
    obj = get_object_or_404(Section, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Section deleted.")
        return redirect('core:section_list')
    return render(request, 'core/school_setup/confirm_delete.html', {
        'obj': obj, 'back_url': 'core:section_list',
    })


# ────────────────────────── SUBJECTS ──────────────────────────

@login_required
@role_required(*_ADMIN)
def subject_list(request):
    q      = request.GET.get('q', '')
    div_id = request.GET.get('division', '')
    qs     = Subject.objects.select_related('grade__division', 'division').all()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(code__icontains=q))
    if div_id:
        qs = qs.filter(division_id=div_id)
    return render(request, 'core/school_setup/subjects.html', {
        'subjects': qs, 'divisions': Division.objects.all(),
        'q': q, 'selected_div': div_id,
    })


@login_required
@role_required(*_ADMIN)
def subject_add(request):
    form = SubjectForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "Subject added.")
        return redirect('core:subject_list')
    return render(request, 'core/school_setup/form.html', {
        'form': form, 'title': 'Add Subject', 'back_url': 'core:subject_list',
    })


@login_required
@role_required(*_ADMIN)
def subject_edit(request, pk):
    obj  = get_object_or_404(Subject, pk=pk)
    form = SubjectForm(request.POST or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, "Subject updated.")
        return redirect('core:subject_list')
    return render(request, 'core/school_setup/form.html', {
        'form': form, 'title': f'Edit: {obj.name}', 'back_url': 'core:subject_list',
    })


@login_required
@role_required(*_ADMIN)
def subject_delete(request, pk):
    obj = get_object_or_404(Subject, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, "Subject deleted.")
        return redirect('core:subject_list')
    return render(request, 'core/school_setup/confirm_delete.html', {
        'obj': obj, 'back_url': 'core:subject_list',
    })


# ────────────────────────── API ENDPOINTS ──────────────────────────

@login_required
def api_grades(request):
    division_id = request.GET.get('division_id')
    if not division_id:
        return JsonResponse({'grades': []})
    grades = list(
        Grade.objects.filter(division_id=division_id, division__is_active=True)
        .values('id', 'name').order_by('order', 'name')
    )
    return JsonResponse({'grades': grades})


@login_required
def api_sections(request):
    grade_id = request.GET.get('grade_id')
    if not grade_id:
        return JsonResponse({'sections': []})
    sections = list(
        Section.objects.filter(grade_id=grade_id)
        .values('id', 'name').order_by('name')
    )
    return JsonResponse({'sections': sections})

