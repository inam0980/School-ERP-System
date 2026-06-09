import csv
import io
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Sum, Count
from django.views.decorators.http import require_POST

from accounts.decorators import role_required
from .models import Student, StudentDocument, Sibling, AuthorizedPickup, PromotionHistory
from .forms import (
    StudentForm, DocumentUploadForm, StudentFilterForm, SiblingForm, AuthorizedPickupForm,
    PromotionFilterForm, IndividualPromotionForm,
)
from fees.models import ExternalCandidate, ExternalCandidatePayment
from core.models import Grade, Division, Board, AcademicYear, Section

_ADMIN   = ('SUPER_ADMIN', 'ADMIN')
_STAFF   = ('SUPER_ADMIN', 'ADMIN', 'TEACHER', 'ACCOUNTANT', 'STAFF')

# Shared column list for blank-template / export / import — keep all three in sync.
STUDENT_CSV_COLUMNS = [
    'Student ID', 'Full Name', 'Arabic Name', 'Gender', 'Date of Birth',
    'Nationality', 'ID Type', 'National ID', 'Iqama Number', 'Passport Number',
    'Religion', 'Birth Place',
    'Division', 'Grade', 'Section', 'Academic Year', 'Roll No.',
    'Enrollment Type', 'Study Mode', 'Fee Category', 'Admission Date', 'Active',
    'Father Name', 'Mother Name', 'Guardian Phone', 'Guardian Email', 'Address',
]

EDUCATION_LEVELS = [
    'Nursery', 'KG1', 'KG2',
    'Grade 1', 'Grade 2', 'Grade 3', 'Grade 4', 'Grade 5', 'Grade 6',
    'Grade 7', 'Grade 8', 'Grade 9', 'Grade 10', 'Grade 11', 'Grade 12',
]

PICKUP_RELATIONS = ['Father', 'Mother', 'Brother', 'Sister', 'Uncle', 'Aunt', 'Grandfather', 'Grandmother', 'Other']


# ────────────────────────── STUDENT HUB ──────────────────────────

@login_required
@role_required(*_STAFF)
def student_hub(request):
    """Landing page: choose Regular Students or External Candidates."""
    regular_count  = Student.objects.count()
    external_count = ExternalCandidate.objects.count()
    return render(request, 'students/student_hub.html', {
        'regular_count':  regular_count,
        'external_count': external_count,
    })


# ────────────────────────── REGULAR STUDENT LIST ──────────────────────────

@login_required
@role_required(*_STAFF)
def student_list(request):
    form = StudentFilterForm(request.GET or None)
    qs   = Student.objects.select_related('division', 'grade', 'section', 'academic_year').all()

    if form.is_valid():
        q         = form.cleaned_data.get('q', '')
        division  = form.cleaned_data.get('division')
        grade     = form.cleaned_data.get('grade')
        section   = form.cleaned_data.get('section')
        gender    = form.cleaned_data.get('gender')
        is_active = form.cleaned_data.get('is_active')

        if q:
            qs = qs.filter(
                Q(full_name__icontains=q) |
                Q(arabic_name__icontains=q) |
                Q(student_id__icontains=q) |
                Q(iqama_number__icontains=q) |
                Q(guardian_phone__icontains=q)
            )
        if division:
            qs = qs.filter(division=division)
        if grade:
            qs = qs.filter(grade=grade)
        if section:
            qs = qs.filter(section=section)
        if gender:
            qs = qs.filter(gender=gender)
        if is_active == '1':
            qs = qs.filter(is_active=True)
        elif is_active == '0':
            qs = qs.filter(is_active=False)

        citizenship = form.cleaned_data.get('citizenship')
        if citizenship == 'saudi':
            qs = qs.filter(nationality='Saudi')
        elif citizenship == 'expat':
            qs = qs.exclude(nationality='Saudi')

    total       = qs.count()
    saudi_count = qs.filter(nationality='Saudi').count()
    expat_count = total - saudi_count
    return render(request, 'students/student_list.html', {
        'students':     qs,
        'form':         form,
        'total':        total,
        'saudi_count':  saudi_count,
        'expat_count':  expat_count,
    })


# ────────────────────────── EXPORT CSV ──────────────────────────

@login_required
@role_required(*_STAFF)
def student_export_csv(request):
    """Export the currently filtered student list as a CSV file."""
    form = StudentFilterForm(request.GET or None)
    qs   = Student.objects.select_related('division', 'grade', 'section', 'academic_year').all()

    if form.is_valid():
        q         = form.cleaned_data.get('q', '')
        division  = form.cleaned_data.get('division')
        grade     = form.cleaned_data.get('grade')
        section   = form.cleaned_data.get('section')
        gender    = form.cleaned_data.get('gender')
        is_active = form.cleaned_data.get('is_active')

        if q:
            qs = qs.filter(
                Q(full_name__icontains=q) |
                Q(arabic_name__icontains=q) |
                Q(student_id__icontains=q) |
                Q(iqama_number__icontains=q) |
                Q(guardian_phone__icontains=q)
            )
        if division:
            qs = qs.filter(division=division)
        if grade:
            qs = qs.filter(grade=grade)
        if section:
            qs = qs.filter(section=section)
        if gender:
            qs = qs.filter(gender=gender)
        if is_active == '1':
            qs = qs.filter(is_active=True)
        elif is_active == '0':
            qs = qs.filter(is_active=False)

        citizenship = form.cleaned_data.get('citizenship')
        if citizenship == 'saudi':
            qs = qs.filter(nationality='Saudi')
        elif citizenship == 'expat':
            qs = qs.exclude(nationality='Saudi')

    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="students.csv"'
    response.write('\ufeff')  # BOM for Excel UTF-8 compatibility

    writer = csv.writer(response)
    writer.writerow(STUDENT_CSV_COLUMNS)
    for s in qs:
        writer.writerow([
            s.student_id, s.full_name, s.arabic_name,
            s.get_gender_display(), s.dob,
            s.nationality, s.get_id_type_display(),
            s.national_id, s.iqama_number, s.passport_number,
            s.get_religion_display() if s.religion else '', s.birth_place,
            s.division, s.grade, s.section, s.academic_year,
            s.roll_number, s.get_enrollment_type_display(),
            s.study_mode.name if s.study_mode else '',
            s.get_fee_category_display(),
            s.admission_date,
            'Yes' if s.is_active else 'No',
            s.father_name, s.mother_name, s.guardian_phone, s.guardian_email,
            s.address,
        ])
    return response


# ────────────────────────── ADD ──────────────────────────

def _save_siblings_from_post(post, student):
    """Parse sibling array fields from POST and bulk-create Sibling records."""
    names    = post.getlist('sibling_full_name[]')
    relations = post.getlist('sibling_relation[]')
    dobs     = post.getlist('sibling_dob[]')
    schools  = post.getlist('sibling_school[]')
    levels   = post.getlist('sibling_level[]')
    to_create = []
    for i, name in enumerate(names):
        name = name.strip()
        if not name:
            continue
        relation = relations[i] if i < len(relations) else ''
        if relation not in ('BROTHER', 'SISTER'):
            continue
        dob = dobs[i].strip() if i < len(dobs) else ''
        to_create.append(Sibling(
            student=student,
            full_name=name,
            relation=relation,
            dob=dob or None,
            current_school=(schools[i].strip() if i < len(schools) else ''),
            educational_level=(levels[i].strip() if i < len(levels) else ''),
        ))
    if to_create:
        Sibling.objects.bulk_create(to_create)


def _save_pickups_from_post(post, student):
    """Parse pickup array fields from POST and bulk-create AuthorizedPickup records."""
    names     = post.getlist('pickup_full_name[]')
    relations = post.getlist('pickup_relation[]')
    phones    = post.getlist('pickup_phone[]')
    to_create = []
    for i, name in enumerate(names):
        name = name.strip()
        if not name:
            continue
        to_create.append(AuthorizedPickup(
            student=student,
            full_name=name,
            relation=(relations[i].strip() if i < len(relations) else ''),
            phone=(phones[i].strip() if i < len(phones) else ''),
        ))
    if to_create:
        AuthorizedPickup.objects.bulk_create(to_create)


@login_required
@role_required(*_ADMIN)
def student_add(request):
    candidate_id = request.GET.get('candidate_id')
    candidate = None
    initial = {}

    if candidate_id:
        from fees.models import ExternalCandidate
        candidate = get_object_or_404(ExternalCandidate, pk=candidate_id)
        if candidate.status == ExternalCandidate.STATUS_APPROVED and candidate.enrolled_student:
            messages.warning(request, "This candidate is already approved and enrolled.")
            return redirect('students:detail', pk=candidate.enrolled_student.pk)

        initial = {
            'full_name': candidate.full_name,
            'arabic_name': candidate.arabic_name,
            'guardian_phone': candidate.phone,
            'nationality': candidate.nationality,
            'national_id': candidate.id_number,
            'grade': candidate.grade_applying,
            'enrollment_type': Student.NEW,
        }

    form = StudentForm(request.POST or None, request.FILES or None, initial=initial)
    if form.is_valid():
        student = form.save(commit=False)
        student.created_by = request.user
        student.save()
        _save_siblings_from_post(request.POST, student)
        _save_pickups_from_post(request.POST, student)

        if candidate:
            candidate.status = ExternalCandidate.STATUS_APPROVED
            candidate.enrolled_student = student
            candidate.save()

        messages.success(request, f"Student {student.full_name} added (ID: {student.student_id}). Please upload identity documents (National ID / Iqama / Passport) below.")
        return redirect('students:detail', pk=student.pk)
    return render(request, 'students/student_form.html', {
        'form': form,
        'title': 'Add Student / إضافة طالب',
        'EDUCATION_LEVELS': EDUCATION_LEVELS,
        'PICKUP_RELATIONS': PICKUP_RELATIONS,
    })


# ────────────────────────── DETAIL ──────────────────────────

@login_required
@role_required(*_STAFF)
def student_detail(request, pk):
    from decimal import Decimal
    from django.db.models import Sum
    from fees.models import StudentFee, Payment

    student = get_object_or_404(Student.objects.select_related(
        'division', 'grade', 'section', 'academic_year', 'created_by'
    ), pk=pk)
    doc_form     = DocumentUploadForm()
    sibling_form = SiblingForm()
    pickup_form  = AuthorizedPickupForm()

    # ── Fee summary ────────────────────────────────────────────────
    fees = (
        StudentFee.objects
        .filter(student=student)
        .select_related('fee_structure__fee_type')
        .order_by('due_date')
    )
    total_charged = fees.exclude(status=StudentFee.WAIVED).aggregate(
        s=Sum('net_amount'))['s'] or Decimal('0.00')
    total_paid = Payment.objects.filter(
        student_fee__student=student).aggregate(
        s=Sum('paid_amount'))['s'] or Decimal('0.00')
    balance_due   = total_charged - total_paid
    overdue_count = fees.filter(status=StudentFee.OVERDUE).count()

    # ── Admission fees paid as external candidate ──────────────────
    admission_payments = []
    try:
        candidate = student.admission_application
        if candidate:
            from fees.models import ExternalCandidatePayment
            admission_payments = list(
                ExternalCandidatePayment.objects.filter(candidate=candidate)
                .order_by('payment_date')
            )
    except Exception:
        pass

    return render(request, 'students/student_detail.html', {
        'student':       student,
        'doc_form':      doc_form,
        'documents':     student.documents.all(),
        'sibling_form':  sibling_form,
        'siblings':      student.siblings.all(),
        'pickup_form':   pickup_form,
        'pickups':       student.authorized_pickups.all(),
        # fee data
        'fees':               fees,
        'total_charged':      total_charged,
        'total_paid':         total_paid,
        'balance_due':        balance_due,
        'overdue_count':      overdue_count,
        'admission_payments': admission_payments,
    })


# ────────────────────────── EDIT ──────────────────────────

@login_required
@role_required(*_ADMIN)
def student_edit(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form    = StudentForm(request.POST or None, request.FILES or None, instance=student)
    if form.is_valid():
        form.save()
        # Replace all siblings with what was submitted
        student.siblings.all().delete()
        _save_siblings_from_post(request.POST, student)
        # Replace all pickups with what was submitted
        student.authorized_pickups.all().delete()
        _save_pickups_from_post(request.POST, student)
        messages.success(request, "Student updated successfully.")
        return redirect('students:detail', pk=student.pk)
    return render(request, 'students/student_form.html', {
        'form': form,
        'student': student,
        'existing_siblings': student.siblings.all(),
        'existing_pickups':  student.authorized_pickups.all(),
        'title': f'Edit: {student.full_name}',
        'EDUCATION_LEVELS': EDUCATION_LEVELS,
        'PICKUP_RELATIONS': PICKUP_RELATIONS,
    })


# ────────────────────────── SOFT DELETE ──────────────────────────

@login_required
@role_required(*_ADMIN)
def student_delete(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student.is_active = False
        student.save(update_fields=['is_active'])
        messages.success(request, f"Student {student.full_name} has been deactivated.")
        return redirect('students:list')
    return render(request, 'students/student_confirm_delete.html', {'student': student})


# ────────────────────────── DOCUMENT UPLOAD ──────────────────────────

@login_required
@role_required(*_ADMIN)
def document_upload(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = DocumentUploadForm(request.POST, request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.student     = student
            doc.uploaded_by = request.user
            doc.save()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'id':       doc.pk,
                    'doc_type': doc.get_doc_type_display(),
                    'filename': doc.filename,
                    'url':      doc.file.url,
                })
            messages.success(request, "Document uploaded.")
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': form.errors}, status=400)
            messages.error(request, "Upload failed. Please check the form.")
    return redirect('students:detail', pk=pk)


@login_required
@role_required(*_ADMIN)
def document_delete(request, doc_pk):
    doc = get_object_or_404(StudentDocument, pk=doc_pk)
    student_pk = doc.student.pk
    if request.method == 'POST':
        doc.file.delete(save=False)
        doc.delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True})
        messages.success(request, "Document deleted.")
    return redirect('students:detail', pk=student_pk)


# ────────────────────────── SIBLING ADD / DELETE ──────────────────────────

@login_required
@role_required(*_ADMIN)
@require_POST
def sibling_add(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = SiblingForm(request.POST)
    if form.is_valid():
        sibling = form.save(commit=False)
        sibling.student = student
        sibling.save()
        messages.success(request, "Sibling added.")
    else:
        messages.error(request, "Please correct the sibling form errors.")
    return redirect('students:detail', pk=pk)


@login_required
@role_required(*_ADMIN)
@require_POST
def sibling_delete(request, sibling_pk):
    sibling = get_object_or_404(Sibling, pk=sibling_pk)
    student_pk = sibling.student.pk
    sibling.delete()
    messages.success(request, "Sibling removed.")
    return redirect('students:detail', pk=student_pk)


# ────────────────────────── AUTHORIZED PICKUP ADD / DELETE ───────────

@login_required
@role_required(*_ADMIN)
@require_POST
def pickup_add(request, pk):
    student = get_object_or_404(Student, pk=pk)
    form = AuthorizedPickupForm(request.POST)
    if form.is_valid():
        pickup = form.save(commit=False)
        pickup.student = student
        pickup.save()
        messages.success(request, "Authorized person added.")
    else:
        messages.error(request, "Please correct the form errors.")
    return redirect('students:detail', pk=pk)


@login_required
@role_required(*_ADMIN)
@require_POST
def pickup_delete(request, pickup_pk):
    pickup = get_object_or_404(AuthorizedPickup, pk=pickup_pk)
    student_pk = pickup.student.pk
    pickup.delete()
    messages.success(request, "Authorized person removed.")
    return redirect('students:detail', pk=student_pk)


# ────────────────────────── ID CARD PRINT ──────────────────────────

@login_required
def student_id_card(request, pk):
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/id_card.html', {'student': student})


@login_required
@role_required(*_STAFF)
def enrollment_contract(request, pk):
    """Printable Student Enrollment Contract (Arabic/English, auto-fill toggle)."""
    student = get_object_or_404(
        Student.objects.select_related('grade', 'section', 'academic_year', 'division'),
        pk=pk,
    )
    return render(request, 'students/enrollment_contract.html', {
        'student': student,
    })


@login_required
@role_required(*_STAFF)
def continuation_agreement(request, pk):
    """Printable continuation agreement for the upcoming academic year."""
    from core.models import AcademicYear
    student = get_object_or_404(
        Student.objects.select_related('grade', 'section', 'academic_year', 'division'),
        pk=pk,
    )
    next_year = AcademicYear.objects.exclude(pk=student.academic_year_id).order_by('-start_date').first()
    return render(request, 'students/continuation_agreement.html', {
        'student':    student,
        'next_year':  next_year,
    })


# ────────────────────────── CSV IMPORT ──────────────────────────

# Reverse maps: CSV display value → model code
_GENDER_MAP = {
    'male / ذكر': 'M', 'male': 'M', 'm': 'M',
    'female / أنثى': 'F', 'female': 'F', 'f': 'F',
}
_ID_TYPE_MAP = {
    'national id / هوية وطنية': 'NATIONAL_ID',
    'national id': 'NATIONAL_ID',
    'iqama / إقامة': 'IQAMA',
    'iqama': 'IQAMA',
    'passport / جواز السفر': 'PASSPORT',
    'passport': 'PASSPORT',
}
_ENROLLMENT_MAP = {
    'new student / طالب جديد': 'NEW',
    'new student': 'NEW',
    'new': 'NEW',
    'transfer / منقول': 'TRANSFER',
    'transfer': 'TRANSFER',
    'regular (continuing) / مستمر': 'REGULAR',
    'regular (continuing)': 'REGULAR',
    'regular': 'REGULAR',
}


@login_required
@role_required(*_ADMIN)
def student_import(request):
    """
    Import students from a CSV file that matches the export format exactly.
    - If Student ID exists in the DB → UPDATE that student.
    - If Student ID is blank or not found → CREATE a new student.
    """
    if request.method == 'POST' and request.FILES.get('csv_file'):
        from core.models import AcademicYear, Division, Grade, Section
        from datetime import date as _date

        try:
            raw = request.FILES['csv_file'].read()
            if raw.startswith(b'\xef\xbb\xbf'):
                raw = raw[3:]          # strip UTF-8 BOM written by export
            reader = csv.DictReader(io.StringIO(raw.decode('utf-8')))

            created = updated = skipped = 0
            errors = []

            for i, raw_row in enumerate(reader, start=2):
                # Strip whitespace from keys and values
                row = {k.strip(): (v.strip() if v else '') for k, v in raw_row.items()}

                full_name = row.get('Full Name', '')
                if not full_name:
                    skipped += 1
                    continue

                try:
                    # ── Dates ─────────────────────────────────────────
                    dob_raw = row.get('Date of Birth', '')
                    try:
                        dob = _date.fromisoformat(dob_raw)
                    except ValueError:
                        errors.append(f"Row {i} ({full_name}): invalid Date of Birth '{dob_raw}'.")
                        continue

                    adm_raw = row.get('Admission Date', '')
                    try:
                        admission_date = _date.fromisoformat(adm_raw) if adm_raw else _date.today()
                    except ValueError:
                        admission_date = _date.today()

                    # ── Coded fields ───────────────────────────────────
                    gender          = _GENDER_MAP.get(row.get('Gender', '').lower(), 'M')
                    id_type         = _ID_TYPE_MAP.get(row.get('ID Type', '').lower(), 'NATIONAL_ID')
                    enrollment_type = _ENROLLMENT_MAP.get(row.get('Enrollment Type', '').lower(), 'NEW')
                    is_active       = row.get('Active', 'Yes').lower() != 'no'

                    # ── FK lookups ─────────────────────────────────────
                    div_name     = row.get('Division', '')
                    grade_name   = row.get('Grade', '')
                    section_name = row.get('Section', '')
                    year_name    = row.get('Academic Year', '')

                    try:
                        division = Division.objects.get(name__iexact=div_name)
                    except Division.DoesNotExist:
                        errors.append(f"Row {i} ({full_name}): Division '{div_name}' not found.")
                        continue

                    try:
                        grade = Grade.objects.get(name__iexact=grade_name, division=division)
                    except Grade.DoesNotExist:
                        errors.append(f"Row {i} ({full_name}): Grade '{grade_name}' not found.")
                        continue

                    try:
                        section = Section.objects.get(name__iexact=section_name, grade=grade)
                    except Section.DoesNotExist:
                        errors.append(f"Row {i} ({full_name}): Section '{section_name}' not found.")
                        continue

                    try:
                        academic_year = AcademicYear.objects.get(name__iexact=year_name)
                    except AcademicYear.DoesNotExist:
                        errors.append(f"Row {i} ({full_name}): Academic Year '{year_name}' not found.")
                        continue

                    # ── Religion / Study Mode / Fee Category mapping ───
                    religion_raw = row.get('Religion', '').strip().lower()
                    religion = ''
                    if 'non' in religion_raw or 'غير' in religion_raw:
                        religion = 'Non-Muslim'
                    elif 'muslim' in religion_raw or 'مسلم' in religion_raw:
                        religion = 'Muslim'

                    study_mode = None
                    sm_name = row.get('Study Mode', '').strip()
                    if sm_name:
                        from core.models import StudyMode
                        study_mode = StudyMode.objects.filter(name__iexact=sm_name, is_active=True).first()

                    fc_raw = row.get('Fee Category', '').strip().lower()
                    fee_category = {
                        'new': 'new', 'regular': 'regular',
                        'transfer': 'transfer', 'other': 'other',
                    }.get(fc_raw, 'regular')

                    # ── Build field dict ───────────────────────────────
                    fields = dict(
                        full_name       = full_name,
                        arabic_name     = row.get('Arabic Name', ''),
                        gender          = gender,
                        dob             = dob,
                        nationality     = row.get('Nationality', 'Saudi Arabia'),
                        id_type         = id_type,
                        national_id     = row.get('National ID', ''),
                        iqama_number    = row.get('Iqama Number', ''),
                        passport_number = row.get('Passport Number', ''),
                        religion        = religion,
                        birth_place     = row.get('Birth Place', ''),
                        division        = division,
                        grade           = grade,
                        section         = section,
                        academic_year   = academic_year,
                        roll_number     = row.get('Roll No.', ''),
                        enrollment_type = enrollment_type,
                        study_mode      = study_mode,
                        fee_category    = fee_category,
                        admission_date  = admission_date,
                        is_active       = is_active,
                        father_name     = row.get('Father Name', ''),
                        mother_name     = row.get('Mother Name', ''),
                        guardian_phone  = row.get('Guardian Phone', ''),
                        guardian_email  = row.get('Guardian Email', ''),
                        address         = row.get('Address', ''),
                    )

                    # ── Create or Update ───────────────────────────────
                    student_id = row.get('Student ID', '')
                    if student_id:
                        n = Student.objects.filter(student_id=student_id).update(**fields)
                        if n:
                            updated += 1
                        else:
                            Student.objects.create(**fields, created_by=request.user)
                            created += 1
                    else:
                        Student.objects.create(**fields, created_by=request.user)
                        created += 1

                except Exception as e:
                    errors.append(f"Row {i} ({full_name}): {e}")

            summary = f"{created} created, {updated} updated"
            if skipped:
                summary += f", {skipped} skipped (blank name)"
            if errors:
                messages.warning(request, f"Import done — {summary}. {len(errors)} error(s): " + " | ".join(errors[:5]))
            else:
                messages.success(request, f"Import complete — {summary}.")

        except Exception as e:
            messages.error(request, f"Import failed: {e}")

        return redirect('students:list')

    return render(request, 'students/student_import.html', {
        'export_url': reverse('students:export_csv'),
    })


# ────────────────────────── CSV TEMPLATE DOWNLOAD ──────────────────────────

@login_required
@role_required(*_ADMIN)
def download_import_template(request):
    """Download a blank CSV with the exact same headers as the student export."""
    response = HttpResponse(content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="students_import_template.csv"'
    response.write('﻿')   # BOM for Excel UTF-8 compatibility
    writer = csv.writer(response)
    writer.writerow(STUDENT_CSV_COLUMNS)
    # Example 1 — Saudi student (National ID)
    writer.writerow([
        '', 'Ahmed Mohammed Ali', 'أحمد محمد علي', 'Male', '2015-09-01',
        'Saudi Arabia', 'National ID', '1234567890', '', '',
        'Muslim', 'Riyadh',
        'American', 'Grade 1', 'A', '2025-26', '01',
        'New Student', 'Regular Mode', 'New', '2025-09-01', 'Yes',
        'Mohammed Ali', 'Fatima Ahmed', '+966501234567', 'parent@email.com',
        'Riyadh, Saudi Arabia',
    ])
    # Example 2 — Non-Saudi student (Iqama)
    writer.writerow([
        '', 'Yusuf Khan', 'يوسف خان', 'Male', '2014-05-20',
        'Pakistan', 'Iqama', '', '2345678901', '',
        'Muslim', 'Karachi',
        'British', 'Grade 2', 'B', '2025-26', '05',
        'Regular (Continuing)', 'Online Mode', 'Regular', '2024-09-01', 'Yes',
        'Imran Khan', 'Aisha Khan', '+966502345678', 'khan@email.com',
        'Jeddah, Saudi Arabia',
    ])
    return response


# ────────────────────────── EXTERNAL CANDIDATE LIST ──────────────────────────

@login_required
@role_required(*_STAFF)
def external_list(request):
    """List all external exam candidates with search."""
    query = request.GET.get('q', '').strip()
    qs = ExternalCandidate.objects.select_related('grade_applying', 'board').annotate(
        payment_count=Count('payments'),
    )

    if query:
        qs = qs.filter(
            Q(full_name__icontains=query) |
            Q(candidate_id__icontains=query) |
            Q(arabic_name__icontains=query) |
            Q(phone__icontains=query) |
            Q(id_number__icontains=query)
        )

    return render(request, 'students/external_list.html', {
        'candidates': qs,
        'total':      qs.count(),
        'query':      query,
    })


# ────────────────────────── EXTERNAL CANDIDATE ADD ──────────────────────────

@login_required
@role_required(*_STAFF)
def external_add(request):
    """Register a new external candidate."""
    grades    = Grade.objects.select_related('division').order_by('division__name', 'order', 'name')
    divisions = Division.objects.filter(is_active=True).order_by('name')

    if request.method == 'POST':
        full_name    = request.POST.get('full_name', '').strip()
        arabic_name  = request.POST.get('arabic_name', '').strip()
        phone        = request.POST.get('phone', '').strip()
        nationality  = request.POST.get('nationality', '').strip()
        id_number    = request.POST.get('id_number', '').strip()
        grade_pk     = request.POST.get('grade_applying', '')
        division_pk  = request.POST.get('division', '')
        notes        = request.POST.get('notes', '').strip()
        is_saudi_val = request.POST.get('is_saudi', '')
        is_saudi     = True if is_saudi_val == 'saudi' else (False if is_saudi_val == 'non_saudi' else None)

        if not full_name:
            messages.error(request, "Full name is required.")
        else:
            grade_obj = None
            if grade_pk:
                try:
                    grade_obj = Grade.objects.get(pk=grade_pk)
                except Grade.DoesNotExist:
                    pass
            division_obj = None
            if division_pk:
                try:
                    division_obj = Division.objects.get(pk=division_pk)
                except Division.DoesNotExist:
                    pass

            candidate = ExternalCandidate.objects.create(
                full_name      = full_name,
                arabic_name    = arabic_name,
                phone          = phone,
                nationality    = nationality,
                id_number      = id_number,
                grade_applying = grade_obj,
                division       = division_obj,
                notes          = notes,
                is_saudi       = is_saudi,
                created_by     = request.user,
            )
            messages.success(request, f"Candidate {candidate.candidate_id} — {candidate.full_name} registered successfully.")
            return redirect('students:external_detail', pk=candidate.pk)

    return render(request, 'students/external_form.html', {
        'grades':    grades,
        'divisions': divisions,
        'candidate': None,
    })


# ────────────────────────── EXTERNAL CANDIDATE EDIT ──────────────────────────

@login_required
@role_required(*_STAFF)
def external_edit(request, pk):
    """Edit an existing external candidate."""
    candidate = get_object_or_404(ExternalCandidate, pk=pk)
    grades    = Grade.objects.select_related('division').order_by('division__name', 'order', 'name')
    divisions = Division.objects.filter(is_active=True).order_by('name')

    if request.method == 'POST':
        full_name    = request.POST.get('full_name', '').strip()
        arabic_name  = request.POST.get('arabic_name', '').strip()
        phone        = request.POST.get('phone', '').strip()
        nationality  = request.POST.get('nationality', '').strip()
        id_number    = request.POST.get('id_number', '').strip()
        grade_pk     = request.POST.get('grade_applying', '')
        division_pk  = request.POST.get('division', '')
        notes        = request.POST.get('notes', '').strip()
        is_saudi_val = request.POST.get('is_saudi', '')
        is_saudi     = True if is_saudi_val == 'saudi' else (False if is_saudi_val == 'non_saudi' else None)

        if not full_name:
            messages.error(request, "Full name is required.")
        else:
            grade_obj = None
            if grade_pk:
                try:
                    grade_obj = Grade.objects.get(pk=grade_pk)
                except Grade.DoesNotExist:
                    pass
            division_obj = None
            if division_pk:
                try:
                    division_obj = Division.objects.get(pk=division_pk)
                except Division.DoesNotExist:
                    pass

            candidate.full_name      = full_name
            candidate.arabic_name    = arabic_name
            candidate.phone          = phone
            candidate.nationality    = nationality
            candidate.id_number      = id_number
            candidate.grade_applying = grade_obj
            candidate.division       = division_obj
            candidate.notes          = notes
            candidate.is_saudi       = is_saudi
            candidate.save()
            messages.success(request, f"Candidate {candidate.full_name} updated.")
            return redirect('students:external_detail', pk=candidate.pk)

    return render(request, 'students/external_form.html', {
        'grades':    grades,
        'divisions': divisions,
        'candidate': candidate,
    })


# ────────────────────────── EXTERNAL CANDIDATE DETAIL ──────────────────────────

@login_required
@role_required(*_STAFF)
def external_detail(request, pk):
    """View details and payment history of an external candidate."""
    candidate = get_object_or_404(
        ExternalCandidate.objects.select_related('grade_applying', 'board'),
        pk=pk,
    )
    payments = ExternalCandidatePayment.objects.filter(
        candidate=candidate,
    ).order_by('-payment_date', '-id')

    total_paid = payments.aggregate(s=Sum('total'))['s'] or 0

    return render(request, 'students/external_detail.html', {
        'candidate':  candidate,
        'payments':   payments,
        'total_paid': total_paid,
    })


# ════════════════════════════════════════════════════════════════════════════
#  PROMOTION  ─  end-of-year bulk + individual student promotion
# ════════════════════════════════════════════════════════════════════════════

from django.db import transaction


def _next_grade(grade):
    """Return the next Grade in the same Division, or None if `grade` is the last."""
    if not grade:
        return None
    return (Grade.objects
            .filter(division=grade.division, order__gt=grade.order)
            .order_by('order')
            .first())


# ──────────────────────────── PROMOTION HUB ────────────────────────────

@login_required
@role_required(*_ADMIN)
def promotion_hub(request):
    """Landing page for the promotion workflow."""
    current_year = AcademicYear.objects.filter(is_current=True).first()
    last_promotion = PromotionHistory.objects.order_by('-promoted_at').first()
    total_promotions = PromotionHistory.objects.count()
    return render(request, 'students/promotion_hub.html', {
        'current_year':     current_year,
        'last_promotion':   last_promotion,
        'total_promotions': total_promotions,
    })


# ──────────────────────────── BULK PROMOTION ────────────────────────────

@login_required
@role_required(*_ADMIN)
def promotion_bulk(request):
    """
    Two-phase screen:
      GET  with ?from_academic_year=&from_division=&from_grade=[&from_section=]
           → list the matching active students with per-row override controls
      POST → commit promotions in a single transaction
    """
    filter_form = PromotionFilterForm(request.GET or None)
    students    = None
    suggested_to_grade = None
    target_year_default = None

    if filter_form.is_valid():
        from_year     = filter_form.cleaned_data['from_academic_year']
        from_division = filter_form.cleaned_data['from_division']
        from_grade    = filter_form.cleaned_data['from_grade']
        from_section  = filter_form.cleaned_data.get('from_section')

        students = (Student.objects
                    .select_related('division', 'grade', 'section', 'academic_year')
                    .filter(academic_year=from_year,
                            division=from_division,
                            grade=from_grade,
                            is_active=True)
                    .order_by('section__name', 'full_name'))
        if from_section:
            students = students.filter(section=from_section)

        suggested_to_grade  = _next_grade(from_grade)
        # default target year = first future year after `from_year`, else current
        target_year_default = (AcademicYear.objects
                               .filter(start_date__gt=from_year.start_date)
                               .order_by('start_date').first()
                               or AcademicYear.objects.filter(is_current=True).first())

    if request.method == 'POST':
        return _process_bulk_promotion(request)

    return render(request, 'students/promotion_bulk.html', {
        'filter_form':         filter_form,
        'students':            students,
        'suggested_to_grade':  suggested_to_grade,
        'target_year_default': target_year_default,
        'academic_years':      AcademicYear.objects.all().order_by('-start_date'),
        'divisions':           Division.objects.filter(is_active=True),
    })


@require_POST
def _process_bulk_promotion(request):
    """Commit the bulk promotion form. Wrapped in a transaction so an error
    rolls everything back — half-promoted cohorts would be a nightmare to clean up."""
    student_ids = request.POST.getlist('student_ids')
    if not student_ids:
        messages.error(request, "No students were selected.")
        return redirect(f"{reverse('students:promotion_bulk')}?{request.POST.urlencode()}")

    default_to_year_id    = request.POST.get('default_to_academic_year') or None
    default_to_division   = request.POST.get('default_to_division') or None
    default_to_grade      = request.POST.get('default_to_grade') or None
    notes_global          = (request.POST.get('notes') or '').strip()

    promoted = retained = transferred = skipped = 0
    errors = []

    try:
        with transaction.atomic():
            for sid in student_ids:
                action = request.POST.get(f'action_{sid}', 'PROMOTE')
                student = Student.objects.select_related('academic_year', 'division', 'grade', 'section').filter(pk=sid).first()
                if not student:
                    skipped += 1
                    continue

                # Snapshot the "from" side
                snap = dict(
                    from_academic_year=student.academic_year,
                    from_division=student.division,
                    from_grade=student.grade,
                    from_section=student.section,
                )

                if action == 'TRANSFER_OUT':
                    student.is_active = False
                    student.save(update_fields=['is_active', 'updated_at'])
                    PromotionHistory.objects.create(
                        student=student, action=PromotionHistory.TRANSFER_OUT,
                        promoted_by=request.user, notes=notes_global,
                        **snap,
                    )
                    transferred += 1
                    continue

                # PROMOTE or RETAIN — both need target year/div/grade/section
                to_year_id     = request.POST.get(f'to_year_{sid}')     or default_to_year_id
                to_division_id = request.POST.get(f'to_division_{sid}') or default_to_division
                to_grade_id    = request.POST.get(f'to_grade_{sid}')    or default_to_grade
                to_section_id  = request.POST.get(f'to_section_{sid}')

                if not all([to_year_id, to_division_id, to_grade_id, to_section_id]):
                    errors.append(f"{student.full_name}: missing target year/division/grade/section")
                    continue

                to_year     = AcademicYear.objects.get(pk=to_year_id)
                to_division = Division.objects.get(pk=to_division_id)
                to_grade    = Grade.objects.get(pk=to_grade_id)
                to_section  = Section.objects.get(pk=to_section_id)

                # Sanity: grade must belong to division, section to grade
                if to_grade.division_id != to_division.pk:
                    errors.append(f"{student.full_name}: grade '{to_grade}' does not belong to division '{to_division}'")
                    continue
                if to_section.grade_id != to_grade.pk:
                    errors.append(f"{student.full_name}: section '{to_section}' does not belong to grade '{to_grade}'")
                    continue

                student.academic_year = to_year
                student.division      = to_division
                student.grade         = to_grade
                student.section       = to_section
                student.enrollment_type = Student.REGULAR
                student.save(update_fields=['academic_year', 'division', 'grade', 'section',
                                            'enrollment_type', 'updated_at'])

                PromotionHistory.objects.create(
                    student=student,
                    action=(PromotionHistory.RETAIN if action == 'RETAIN' else PromotionHistory.PROMOTE),
                    promoted_by=request.user,
                    notes=notes_global,
                    to_academic_year=to_year, to_division=to_division,
                    to_grade=to_grade, to_section=to_section,
                    **snap,
                )
                if action == 'RETAIN':
                    retained += 1
                else:
                    promoted += 1

            if errors:
                # roll back the whole batch — caller must fix issues and retry
                raise ValueError("validation_errors")

    except ValueError:
        for e in errors:
            messages.error(request, e)
        messages.error(request, "Nothing was saved — fix the issues above and try again.")
        return redirect(f"{reverse('students:promotion_bulk')}?{request.GET.urlencode()}")

    parts = []
    if promoted:    parts.append(f"{promoted} promoted")
    if retained:    parts.append(f"{retained} retained")
    if transferred: parts.append(f"{transferred} transferred out")
    if skipped:     parts.append(f"{skipped} skipped")
    messages.success(request, "Promotion complete: " + (", ".join(parts) or "no changes."))
    return redirect('students:promotion_hub')


# ──────────────────────────── INDIVIDUAL PROMOTION ────────────────────────────

@login_required
@role_required(*_ADMIN)
def promotion_individual(request, pk):
    """Promote a single student. Linked from the student detail page."""
    student = get_object_or_404(
        Student.objects.select_related('academic_year', 'division', 'grade', 'section'),
        pk=pk,
    )
    suggested_grade = _next_grade(student.grade)

    if request.method == 'POST':
        form = IndividualPromotionForm(request.POST)
        if form.is_valid():
            action = form.cleaned_data['action']
            snap = dict(
                from_academic_year=student.academic_year,
                from_division=student.division,
                from_grade=student.grade,
                from_section=student.section,
            )
            if action == 'TRANSFER_OUT':
                student.is_active = False
                student.save(update_fields=['is_active', 'updated_at'])
                PromotionHistory.objects.create(
                    student=student, action=PromotionHistory.TRANSFER_OUT,
                    promoted_by=request.user, notes=form.cleaned_data['notes'],
                    **snap,
                )
                messages.success(request, f"{student.full_name} marked as transferred out.")
                return redirect('students:detail', pk=student.pk)

            to_year     = form.cleaned_data['to_academic_year']
            to_division = form.cleaned_data['to_division']
            to_grade    = form.cleaned_data['to_grade']
            to_section  = form.cleaned_data['to_section']

            if to_grade.division_id != to_division.pk:
                form.add_error('to_grade', "Selected grade does not belong to the selected division.")
            elif to_section.grade_id != to_grade.pk:
                form.add_error('to_section', "Selected section does not belong to the selected grade.")
            else:
                with transaction.atomic():
                    student.academic_year   = to_year
                    student.division        = to_division
                    student.grade           = to_grade
                    student.section         = to_section
                    student.enrollment_type = Student.REGULAR
                    student.save(update_fields=['academic_year', 'division', 'grade',
                                                'section', 'enrollment_type', 'updated_at'])
                    PromotionHistory.objects.create(
                        student=student,
                        action=(PromotionHistory.RETAIN if action == 'RETAIN' else PromotionHistory.PROMOTE),
                        promoted_by=request.user, notes=form.cleaned_data['notes'],
                        to_academic_year=to_year, to_division=to_division,
                        to_grade=to_grade, to_section=to_section,
                        **snap,
                    )
                label = "retained" if action == 'RETAIN' else "promoted"
                messages.success(request, f"{student.full_name} {label} successfully.")
                return redirect('students:detail', pk=student.pk)
    else:
        # Pre-fill: next year + suggested next grade in same division
        next_year = (AcademicYear.objects
                     .filter(start_date__gt=student.academic_year.start_date)
                     .order_by('start_date').first()
                     or AcademicYear.objects.filter(is_current=True).first())
        form = IndividualPromotionForm(initial={
            'action': 'PROMOTE',
            'to_academic_year': next_year,
            'to_division': student.division,
            'to_grade': suggested_grade,
        })

    return render(request, 'students/promotion_individual.html', {
        'student':         student,
        'form':            form,
        'suggested_grade': suggested_grade,
        'history':         student.promotion_history.select_related(
                              'from_grade', 'from_section', 'to_grade', 'to_section'
                          ).all()[:20],
    })


# ─────────── AJAX helpers used by the cascading selects ───────────

@login_required
@role_required(*_STAFF)
def ajax_grades_for_division(request):
    """GET /students/promotion/ajax/grades/?division=<id>  →  JSON list."""
    division_id = request.GET.get('division')
    grades = Grade.objects.filter(division_id=division_id).order_by('order', 'name') if division_id else Grade.objects.none()
    return JsonResponse({'grades': [{'id': g.pk, 'name': g.name} for g in grades]})


@login_required
@role_required(*_STAFF)
def ajax_sections_for_grade(request):
    """GET /students/promotion/ajax/sections/?grade=<id>  →  JSON list."""
    grade_id = request.GET.get('grade')
    sections = Section.objects.filter(grade_id=grade_id).order_by('name') if grade_id else Section.objects.none()
    return JsonResponse({'sections': [{'id': s.pk, 'name': s.name} for s in sections]})

