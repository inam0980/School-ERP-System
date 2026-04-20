import io
import csv
from decimal import Decimal
from datetime import date, timedelta

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.db.models import Q, Sum, Count
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.core.cache import cache

from accounts.decorators import role_required
from students.models import Student
from core.models import AcademicYear, Division, Grade, Section
from .models import (
    FeeType, FeeStructure, FeeStructureItem, FeeStructureBundle, BundleInstallment,
    StudentFee, Payment, TaxInvoice, Salary,
    TuitionFeeConfig, TuitionInstallment,
    PaymentPlan, PaymentPlanInstallment,
)
from .forms import (
    FeeTypeForm, FeeStructureForm, FeeStructureBulkCreateForm,
    FeeStructureBundleForm, BundleInstallmentForm,
    BulkAssignFeeForm,
    StudentFeeEditForm, PaymentForm, FeeReportFilterForm,
    SalaryForm, SalaryMonthFilterForm,
    ManualInvoiceHeaderForm, ManualInvoiceLineForm, DefaultersFilterForm,
    TuitionFeeConfigForm, TuitionInstallmentFormSet, TuitionConfigFilterForm,
)

_ADMIN       = ('SUPER_ADMIN', 'ADMIN')
_ACCOUNTANT  = ('SUPER_ADMIN', 'ADMIN', 'ACCOUNTANT')
_STAFF_VIEW  = ('SUPER_ADMIN', 'ADMIN', 'ACCOUNTANT', 'STAFF')


def _grades_by_division():
    """Return list of (division, [grade, ...]) ordered for optgroup display."""
    result = {}
    for grade in Grade.objects.select_related('division').order_by('division__name', 'order', 'name'):
        result.setdefault(grade.division, []).append(grade)
    return list(result.items())


# ════════════════════════════════════════════════════════════════
#  DASHBOARD SUMMARY (JSON for dashboard widget)
# ════════════════════════════════════════════════════════════════

@login_required
def api_fees_summary(request):
    cached = cache.get('fees_dashboard_summary')
    if cached is not None:
        return JsonResponse(cached)

    today    = timezone.localdate()
    overdue  = StudentFee.objects.filter(status='OVERDUE').count()
    today_total = Payment.objects.filter(payment_date=today).aggregate(
        s=Sum('paid_amount'))['s'] or 0
    month_total = Payment.objects.filter(
        payment_date__year=today.year,
        payment_date__month=today.month,
    ).aggregate(s=Sum('paid_amount'))['s'] or 0
    data = {
        'overdue':     overdue,
        'today':       float(today_total),
        'this_month':  float(month_total),
    }
    cache.set('fees_dashboard_summary', data, 300)
    return JsonResponse(data)


# ════════════════════════════════════════════════════════════════
#  FEE TYPE CRUD
# ════════════════════════════════════════════════════════════════

@login_required
@role_required(*_ADMIN)
def fee_type_list(request):
    types = FeeType.objects.all()
    return render(request, 'fees/fee_type_list.html', {'fee_types': types})


@login_required
@role_required(*_ADMIN)
def fee_type_form(request, pk=None):
    instance = get_object_or_404(FeeType, pk=pk) if pk else None
    form     = FeeTypeForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, "Fee type saved.")
        return redirect('fees:fee_type_list')
    return render(request, 'fees/fee_type_form.html', {
        'form': form, 'title': 'Edit Fee Type' if instance else 'Add Fee Type',
    })


@login_required
@role_required(*_ADMIN)
@require_POST
def fee_type_delete(request, pk):
    get_object_or_404(FeeType, pk=pk).delete()
    messages.success(request, "Fee type deleted.")
    return redirect('fees:fee_type_list')


# ════════════════════════════════════════════════════════════════
#  FEE STRUCTURE CRUD
# ════════════════════════════════════════════════════════════════

@login_required
@role_required(*_ACCOUNTANT)
def fee_structure_list(request):
    year_id = request.GET.get('year')
    qs = FeeStructure.objects.select_related(
        'academic_year', 'grade__division'
    ).prefetch_related('items__fee_type')
    if year_id:
        qs = qs.filter(academic_year_id=year_id)

    # Group by division for display
    divisions_map = {}
    for s in qs:
        div = s.grade.division
        divisions_map.setdefault(div, []).append(s)

    return render(request, 'fees/fee_structure_list.html', {
        'divisions_map': divisions_map,
        'years':         AcademicYear.objects.all(),
        'active_year':   year_id,
    })


@login_required
@role_required(*_ADMIN)
def fee_structure_form(request, pk=None):
    # ── EDIT: single existing structure ──────────────────────────
    if pk:
        instance = get_object_or_404(FeeStructure, pk=pk)
        all_fee_types = FeeType.objects.all()
        existing_items = {item.fee_type_id: item for item in instance.items.select_related('fee_type')}

        form = FeeStructureForm(request.POST or None, instance=instance)
        if request.method == 'POST' and form.is_valid():
            form.save()
            for ft in all_fee_types:
                raw = request.POST.get(f'amount_{ft.pk}', '').strip()
                if raw:
                    try:
                        amt = Decimal(raw)
                    except Exception:
                        amt = None
                    if amt and amt > 0:
                        if ft.pk in existing_items:
                            item = existing_items[ft.pk]
                            item.amount = amt
                            item.save()
                        else:
                            FeeStructureItem.objects.create(structure=instance, fee_type=ft, amount=amt)
                    else:
                        if ft.pk in existing_items:
                            existing_items[ft.pk].delete()
                else:
                    if ft.pk in existing_items:
                        existing_items[ft.pk].delete()
            messages.success(request, "Fee structure saved.")
            return redirect('fees:fee_structure_list')

        fee_types_with_amounts = [
            {'ft': ft, 'amount': existing_items[ft.pk].amount if ft.pk in existing_items else ''}
            for ft in all_fee_types
        ]
        grades_by_division = _grades_by_division()
        return render(request, 'fees/fee_structure_form.html', {
            'form': form, 'instance': instance, 'title': 'Edit Fee Structure',
            'fee_types_with_amounts': fee_types_with_amounts,
            'grades_by_division': grades_by_division,
        })

    # ── CREATE: one structure per grade ────────────────────────────────
    form = FeeStructureBulkCreateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        grade         = form.cleaned_data['grade']
        academic_year = form.cleaned_data['academic_year']
        frequency     = form.cleaned_data['frequency']
        name          = form.cleaned_data.get('name', '')

        # Collect per-fee-type amounts from raw POST (amount_<ft_pk>)
        all_fee_types = FeeType.objects.all()
        items_to_create = []  # list of (FeeType, Decimal amount)
        for ft in all_fee_types:
            raw = request.POST.get(f'amount_{ft.pk}', '').strip()
            if raw:
                try:
                    amt = Decimal(raw)
                except Exception:
                    amt = None
                if amt and amt > 0:
                    items_to_create.append((ft, amt))

        if not items_to_create:
            messages.error(request, 'Enter an amount for at least one fee type.')
        else:
            container, new_s = FeeStructure.objects.get_or_create(
                academic_year=academic_year,
                grade=grade,
                defaults={'name': name, 'frequency': frequency},
            )
            items_created = items_skipped = 0
            for ft, amt in items_to_create:
                _, new_i = FeeStructureItem.objects.get_or_create(
                    structure=container,
                    fee_type=ft,
                    defaults={'amount': amt},
                )
                if new_i:
                    items_created += 1
                else:
                    items_skipped += 1

            verb = 'created' if new_s else 'already existed'
            messages.success(
                request,
                f"Structure '{container}' {verb}. "
                f"{items_created} fee-type item(s) added"
                + (f", {items_skipped} skipped (already existed)." if items_skipped else '.')
            )
            return redirect('fees:fee_structure_list')

    all_fee_types = FeeType.objects.all()
    grades_by_division = _grades_by_division()

    return render(request, 'fees/fee_structure_form.html', {
        'form':            form,
        'instance':        None,
        'title':           'Add Fee Structure',
        'all_fee_types':   all_fee_types,
        'grades_by_division': grades_by_division,
    })


@login_required
@role_required(*_ADMIN)
@require_POST
def fee_structure_delete(request, pk):
    get_object_or_404(FeeStructure, pk=pk).delete()
    messages.success(request, "Fee structure deleted.")
    return redirect('fees:fee_structure_list')


# ════════════════════════════════════════════════════════════════
#  FEE STRUCTURE BUNDLE  (all-in-one: entrance + registration + tuition)
# ════════════════════════════════════════════════════════════════

@login_required
@role_required(*_ACCOUNTANT)
def bundle_list(request):
    year_id = request.GET.get('year', '')
    qs = (FeeStructureBundle.objects
          .select_related('academic_year', 'division', 'grade', 'created_by')
          .prefetch_related('installments'))
    if year_id:
        qs = qs.filter(academic_year_id=year_id)
    return render(request, 'fees/bundle_list.html', {
        'bundles':     qs,
        'years':       AcademicYear.objects.all(),
        'active_year': year_id,
    })


@login_required
@role_required(*_ADMIN)
def bundle_form(request, pk=None):
    instance = get_object_or_404(FeeStructureBundle, pk=pk) if pk else None
    form     = FeeStructureBundleForm(request.POST or None, instance=instance)

    if form.is_valid():
        bundle = form.save(commit=False)
        if not instance:
            bundle.created_by = request.user
        bundle.save()
        bundle.generate_installments()
        messages.success(request, f"Bundle '{bundle.name}' saved — instalments auto-generated.")
        return redirect('fees:bundle_detail', pk=bundle.pk)

    return render(request, 'fees/bundle_form.html', {
        'form':     form,
        'instance': instance,
        'title':    'Edit Fee Structure Bundle' if instance else 'Create Fee Structure Bundle',
    })


@login_required
@role_required(*_ACCOUNTANT)
def bundle_detail(request, pk):
    bundle = get_object_or_404(
        FeeStructureBundle.objects
        .select_related('academic_year', 'division', 'grade', 'created_by')
        .prefetch_related('installments'),
        pk=pk,
    )

    # ── Save edited instalments ──────────────────────────────────
    if request.method == 'POST' and 'save_installments' in request.POST:
        errors = []
        for inst in bundle.installments.all():
            raw_amt   = request.POST.get(f'inst_amount_{inst.pk}', '').strip()
            raw_due   = request.POST.get(f'inst_due_{inst.pk}', '').strip()
            raw_label = request.POST.get(f'inst_label_{inst.pk}', inst.label).strip()
            try:
                amt = Decimal(raw_amt)
                if amt <= 0:
                    raise ValueError
            except Exception:
                errors.append(f'Instalment #{inst.installment_no}: invalid amount.')
                continue
            if inst.installment_no == 1 and amt < bundle.min_down_payment:
                errors.append(
                    f'Down payment must be at least SAR {bundle.min_down_payment:.2f}.'
                )
                continue
            try:
                due = date.fromisoformat(raw_due) if raw_due else inst.due_date
            except Exception:
                due = inst.due_date
            inst.amount   = amt
            inst.due_date = due
            inst.label    = raw_label or inst.label
            inst.save()

        if errors:
            for e in errors:
                messages.error(request, e)
        else:
            messages.success(request, 'Instalments updated successfully.')
        return redirect('fees:bundle_detail', pk=bundle.pk)

    # ── Regenerate instalments (reset to equal splits) ───────────
    if request.method == 'POST' and 'regenerate' in request.POST:
        bundle.generate_installments()
        messages.success(request, 'Instalments regenerated with equal splits.')
        return redirect('fees:bundle_detail', pk=bundle.pk)

    sections = Section.objects.filter(grade=bundle.grade).order_by('name')
    return render(request, 'fees/bundle_detail.html', {
        'bundle':   bundle,
        'sections': sections,
    })


@login_required
@role_required(*_ACCOUNTANT)
@require_POST
def bundle_assign(request, pk):
    """
    Assign a FeeStructureBundle to all active students in its Division+Grade
    (optionally filtered to one Section).
    Creates FeeStructure records per fee type and StudentFee records per student.
    For tuition, creates a PaymentPlan with the bundle's instalments.
    """
    bundle     = get_object_or_404(FeeStructureBundle, pk=pk)
    section_id = request.POST.get('section_id', '').strip()

    students = Student.objects.filter(
        grade=bundle.grade,
        division=bundle.division,
        is_active=True,
    )
    if section_id:
        students = students.filter(section_id=section_id)

    if not students.exists():
        messages.warning(request, 'No active students found for this bundle\'s Division / Grade.')
        return redirect('fees:bundle_detail', pk=bundle.pk)

    # ── Get or create the three FeeType objects ──────────────────
    ft_entrance, _ = FeeType.objects.get_or_create(
        category=FeeType.ENTRANCE_EXAM,
        defaults={'name': 'Grade Level Entrance Exam Fee', 'is_taxable': False},
    )
    ft_reg, _ = FeeType.objects.get_or_create(
        category=FeeType.REGISTRATION,
        defaults={'name': 'Registration Fee', 'is_taxable': False},
    )
    ft_tuition, _ = FeeType.objects.get_or_create(
        category=FeeType.TUITION,
        defaults={'name': 'Tuition Fee', 'is_taxable': True},
    )

    # ── Get or create one FeeStructure container + items ─────────
    container, _ = FeeStructure.objects.get_or_create(
        academic_year=bundle.academic_year,
        grade=bundle.grade,
        defaults={'name': bundle.name, 'frequency': 'ANNUAL'},
    )

    fsi_entrance = fsi_reg = None
    if bundle.entrance_exam_fee > 0:
        fsi_entrance, _ = FeeStructureItem.objects.get_or_create(
            structure=container, fee_type=ft_entrance,
            defaults={'amount': bundle.entrance_exam_fee},
        )
    if bundle.registration_fee > 0:
        fsi_reg, _ = FeeStructureItem.objects.get_or_create(
            structure=container, fee_type=ft_reg,
            defaults={'amount': bundle.registration_fee},
        )
    fsi_tuition, _ = FeeStructureItem.objects.get_or_create(
        structure=container, fee_type=ft_tuition,
        defaults={'amount': bundle.gross_tuition_fee},
    )

    created = skipped = 0
    installments = list(bundle.installments.order_by('installment_no'))

    for student in students:
        # 1 — Entrance exam fee (skip if zero)
        if fsi_entrance:
            sf, new = StudentFee.objects.get_or_create(
                student=student, fee_structure=fsi_entrance,
                defaults={
                    'amount':      bundle.entrance_exam_fee,
                    'discount':    Decimal('0'),
                    'due_date':    bundle.due_date,
                    'assigned_by': request.user,
                },
            )
            if new:
                sf.save()
                created += 1
            else:
                skipped += 1

        # 2 — Registration fee (skip if zero)
        if fsi_reg:
            sf, new = StudentFee.objects.get_or_create(
                student=student, fee_structure=fsi_reg,
                defaults={
                    'amount':      bundle.registration_fee,
                    'discount':    Decimal('0'),
                    'due_date':    bundle.due_date,
                    'assigned_by': request.user,
                },
            )
            if new:
                sf.save()
                created += 1
            else:
                skipped += 1

        # 3 — Tuition fee (with group discount + optional payment plan)
        sf_tuition, new = StudentFee.objects.get_or_create(
            student=student, fee_structure=fsi_tuition,
            defaults={
                'amount':        bundle.gross_tuition_fee,
                'discount':      bundle.group_discount_amount,
                'discount_note': f'Group discount {bundle.group_discount_pct}%',
                'due_date':      bundle.due_date,
                'assigned_by':   request.user,
            },
        )
        if new:
            sf_tuition.save()  # triggers net_amount calc
            created += 1
            # Create PaymentPlan with bundle instalments (if > 1 instalment)
            if len(installments) > 1:
                plan = PaymentPlan.objects.create(
                    student_fee=sf_tuition,
                    notes=f'Bundle: {bundle.name}',
                    created_by=request.user,
                )
                for binst in installments:
                    PaymentPlanInstallment.objects.create(
                        plan=plan,
                        installment_no=binst.installment_no,
                        amount=binst.amount,
                        due_date=binst.due_date,
                    )
        else:
            skipped += 1

    messages.success(
        request,
        f'Assignment done — {created} fee record(s) created, {skipped} already existed.'
    )
    return redirect('fees:bundle_detail', pk=bundle.pk)


@login_required
@role_required(*_ADMIN)
@require_POST
def bundle_delete(request, pk):
    bundle = get_object_or_404(FeeStructureBundle, pk=pk)
    name   = bundle.name
    bundle.delete()
    messages.success(request, f"Bundle '{name}' deleted.")
    return redirect('fees:bundle_list')




@login_required
@role_required(*_ACCOUNTANT)
def fee_structure_items_json(request, pk):
    """AJAX: return fee items for a given FeeStructure pk."""
    structure = get_object_or_404(
        FeeStructure.objects.select_related('academic_year', 'grade__division'), pk=pk
    )
    items = list(
        structure.items.select_related('fee_type').values(
            'id', 'fee_type__name', 'fee_type__is_taxable', 'amount'
        )
    )
    return JsonResponse({
        'structure': str(structure),
        'grade':     str(structure.grade),
        'division':  str(structure.grade.division),
        'items': [
            {
                'id':         i['id'],
                'fee_type':   i['fee_type__name'],
                'is_taxable': i['fee_type__is_taxable'],
                'amount':     str(i['amount']),
            } for i in items
        ],
    })


@login_required
@role_required(*_ACCOUNTANT)
def bulk_assign_fees(request):
    form    = BulkAssignFeeForm(request.POST or None)
    results = None

    if form.is_valid():
        structure    = form.cleaned_data['fee_structure']   # FeeStructure container
        discount_pct = form.cleaned_data['discount_pct']   # Decimal 0-100
        due_date     = form.cleaned_data['due_date']

        items = list(structure.items.select_related('fee_type').all())
        if not items:
            messages.warning(request, 'This fee structure has no fee-type items yet.')
            return redirect('fees:fee_structure_list')

        # Filter students by the structure's grade (division is implicit via grade)
        students = Student.objects.filter(
            grade=structure.grade, is_active=True
        )

        created = skipped = 0
        assigned_students = []
        for student in students:
            student_created = False
            for item in items:
                discount_amt = (item.amount * discount_pct / 100).quantize(Decimal('0.01'))
                disc_note    = f'{discount_pct}% bulk discount' if discount_pct > 0 else ''
                obj, created_flag = StudentFee.objects.get_or_create(
                    student=student,
                    fee_structure=item,
                    defaults={
                        'amount':        item.amount,
                        'discount':      discount_amt,
                        'discount_note': disc_note,
                        'due_date':      due_date,
                        'assigned_by':   request.user,
                    },
                )
                if created_flag:
                    obj.save()   # triggers net_amount + VAT calc
                    created += 1
                    student_created = True
                else:
                    skipped += 1
            if student_created and student not in assigned_students:
                assigned_students.append(student)

        results = {'created': created, 'skipped': skipped, 'students': assigned_students, 'structure': structure}
        messages.success(
            request,
            f"Done — {created} fee records created, {skipped} already existed."
        )

    # Load items for the currently selected structure (for JS preview)
    selected_structure = None
    structure_items    = []
    if request.method == 'POST' and form.is_valid():
        pass  # already handled above
    elif request.method == 'POST':
        pk_val = request.POST.get('fee_structure')
        if pk_val:
            try:
                selected_structure = FeeStructure.objects.get(pk=pk_val)
                structure_items = list(selected_structure.items.select_related('fee_type'))
            except FeeStructure.DoesNotExist:
                pass

    # Build JSON map: structure_pk → {grade_name, division_pk, year_pk, sections:[{pk,name}]}
    import json as _json
    structures_qs = FeeStructure.objects.select_related(
        'grade__division', 'academic_year'
    ).prefetch_related('grade__sections')
    structure_meta_map = {}
    for fs in structures_qs:
        structure_meta_map[str(fs.pk)] = {
            'grade':       str(fs.grade),
            'division_pk': str(fs.grade.division_id),
            'year_pk':     str(fs.academic_year_id),
            'sections': [
                {'pk': str(sec.pk), 'name': sec.name}
                for sec in fs.grade.sections.order_by('name')
            ],
        }

    from core.models import AcademicYear
    years     = AcademicYear.objects.order_by('-start_date')
    divisions = Division.objects.order_by('name')

    # ── Past assignment summary: group StudentFee by fee structure ──
    from django.db.models import Count, Max
    past_assignments = (
        StudentFee.objects
        .values(
            'fee_structure__structure__pk',
            'fee_structure__structure__academic_year__name',
            'fee_structure__structure__grade__name',
            'fee_structure__structure__grade__division__name',
        )
        .annotate(
            student_count=Count('student', distinct=True),
            last_assigned=Max('created_at'),
        )
        .exclude(fee_structure__structure__grade__division__name='ADHOC')
        .order_by('-last_assigned')
    )

    return render(request, 'fees/bulk_assign.html', {
        'form': form, 'results': results,
        'structure_items': structure_items,
        'structure_meta_map_json': _json.dumps(structure_meta_map),
        'years':          years,
        'divisions':      divisions,
        'past_assignments': past_assignments,
    })


# ════════════════════════════════════════════════════════════════
#  FEE COLLECTION
# ════════════════════════════════════════════════════════════════

@login_required
@role_required(*_ACCOUNTANT)
def fee_collection(request):
    """
    Multi-fee payment: search student → see all outstanding fees with
    checkboxes and per-row amount/discount → one submit pays them all.

    Also supports hierarchical browse: Division → Grade → Section → Students.
    """
    import json as _json

    query    = request.GET.get('q', '').strip()
    students = []
    student  = None
    dues     = []

    # ── Browse params ───────────────────────────────────────────
    browse_div_id     = request.GET.get('div', '')
    browse_grade_id   = request.GET.get('grade', '')
    browse_section_id = request.GET.get('section', '')

    # Build browse data for the template (all divisions + their grades/sections)
    all_divisions = list(
        Division.objects.filter(is_active=True)
        .prefetch_related('grades__sections')
        .order_by('name')
    )
    browse_data = []
    for div in all_divisions:
        grades_data = []
        for gr in div.grades.order_by('order', 'name'):
            sections_data = [
                {'id': sec.pk, 'name': sec.name}
                for sec in gr.sections.order_by('name')
            ]
            grades_data.append({'id': gr.pk, 'name': gr.name, 'sections': sections_data})
        browse_data.append({'id': div.pk, 'name': str(div), 'grades': grades_data})

    # ── Name / ID search ────────────────────────────────────────
    if query:
        students = Student.objects.filter(
            Q(full_name__icontains=query) |
            Q(student_id__icontains=query) |
            Q(arabic_name__icontains=query),
            is_active=True,
        ).select_related('grade', 'section', 'division')[:40]

    # ── Browse: Section selected → show all students in it ──────
    elif browse_section_id:
        students = Student.objects.filter(
            section_id=browse_section_id,
            is_active=True,
        ).select_related('grade', 'section', 'division').order_by('full_name')

    # ── Browse: Grade selected (no section) → show all students in grade ──
    elif browse_grade_id:
        students = Student.objects.filter(
            grade_id=browse_grade_id,
            is_active=True,
        ).select_related('grade', 'section', 'division').order_by('section__name', 'full_name')

    student_pk = request.GET.get('student_id') or request.POST.get('student_id')
    if student_pk:
        students = []   # hide the list once a student is selected
        student = get_object_or_404(
            Student.objects.select_related('grade', 'section', 'division', 'academic_year'),
            pk=student_pk,
        )
        dues = list(
            StudentFee.objects.filter(student=student)
            .exclude(status__in=['WAIVED', 'PAID'])
            .select_related('fee_structure', 'fee_structure__fee_type')
            .prefetch_related('payment_plan__installments')
            .order_by('due_date')
        )
        for sf in dues:
            sf.discount_pct = (
                (sf.discount / sf.amount * 100).quantize(Decimal('0.01'))
                if sf.amount else Decimal('0.00')
            )

    # ── MULTI-FEE POST ──────────────────────────────────────────
    receipts = []
    if request.method == 'POST' and student:
        selected_pks       = request.POST.getlist('selected_fees')
        selected_inst_pks  = request.POST.getlist('selected_installments')

        if not selected_pks and not selected_inst_pks:
            messages.error(request, "Please select at least one fee to pay.")
        else:
            date_str = request.POST.get('payment_date', '')
            try:
                payment_date = date.fromisoformat(date_str) if date_str else timezone.localdate()
            except ValueError:
                payment_date = timezone.localdate()

            payment_method  = request.POST.get('payment_method', Payment.CASH)
            transaction_ref = request.POST.get('transaction_ref', '').strip()
            notes           = request.POST.get('notes', '').strip()
            errors          = []

            # ── Normal (non-plan) fees ───────────────────────────
            for pk in selected_pks:
                try:
                    fee = StudentFee.objects.select_related(
                        'fee_structure__fee_type').get(pk=pk, student=student)
                except StudentFee.DoesNotExist:
                    continue

                raw_pct = request.POST.get(f'discount_pct_{pk}', '').strip()
                try:
                    pct = Decimal(raw_pct) if raw_pct else Decimal('0')
                except Exception:
                    pct = Decimal('0')
                disc = (pct / 100 * fee.amount).quantize(Decimal('0.01'))
                if disc != (fee.discount or Decimal('0')):
                    fee.discount      = disc
                    fee.discount_note = request.POST.get(f'discount_note_{pk}', '').strip()
                    fee.save()

                raw_amt = request.POST.get(f'amount_{pk}', '').strip()
                try:
                    amount = Decimal(raw_amt)
                except Exception:
                    errors.append(f"{fee.fee_structure.fee_type.name}: invalid amount entered.")
                    continue

                if amount <= 0:
                    errors.append(f"{fee.fee_structure.fee_type.name}: amount must be greater than 0.")
                    continue
                if amount > fee.balance:
                    errors.append(
                        f"{fee.fee_structure.fee_type.name}: SAR {amount} exceeds "
                        f"balance of SAR {fee.balance:.2f}."
                    )
                    continue

                payment = Payment.objects.create(
                    student_fee     = fee,
                    paid_amount     = amount,
                    payment_date    = payment_date,
                    payment_method  = payment_method,
                    transaction_ref = transaction_ref,
                    notes           = notes,
                    collected_by    = request.user,
                )
                fee.refresh_status()
                receipts.append(payment)

            # ── Installment plan payments ────────────────────────
            for inst_pk in selected_inst_pks:
                try:
                    inst = PaymentPlanInstallment.objects.select_related(
                        'plan__student_fee__fee_structure__fee_type',
                        'plan__student_fee__student',
                    ).get(pk=inst_pk, plan__student_fee__student=student)
                except PaymentPlanInstallment.DoesNotExist:
                    continue

                if inst.balance <= 0:
                    continue

                raw_amt = request.POST.get(f'inst_amount_{inst_pk}', '').strip()
                try:
                    amount = Decimal(raw_amt)
                except Exception:
                    errors.append(
                        f"Installment {inst.installment_no} of "
                        f"{inst.plan.student_fee.fee_structure.fee_type.name}: "
                        f"invalid amount."
                    )
                    continue

                if amount <= 0 or amount > inst.balance:
                    errors.append(
                        f"Installment {inst.installment_no}: SAR {amount} "
                        f"exceeds balance SAR {inst.balance:.2f}."
                    )
                    continue

                # Record payment against the parent StudentFee
                payment = Payment.objects.create(
                    student_fee     = inst.plan.student_fee,
                    paid_amount     = amount,
                    payment_date    = payment_date,
                    payment_method  = payment_method,
                    transaction_ref = transaction_ref,
                    notes           = f"Installment {inst.installment_no}" + (f" — {notes}" if notes else ""),
                    collected_by    = request.user,
                )
                # Update installment paid amount & status
                inst.paid_amount = (inst.paid_amount + amount).quantize(Decimal('0.01'))
                inst.save(update_fields=['paid_amount'])
                inst.refresh_status()
                inst.plan.student_fee.refresh_status()
                receipts.append(payment)

            for e in errors:
                messages.error(request, e)

            if receipts:
                total = sum(p.paid_amount for p in receipts)
                messages.success(
                    request,
                    f"{len(receipts)} payment(s) recorded — Total collected: SAR {total:.2f}"
                )
                receipt_pks = ','.join(str(p.pk) for p in receipts)
                return redirect(
                    f"{request.path}?student_id={student.pk}&receipts={receipt_pks}"
                )

    # Load receipts if redirected back after payment
    receipt_pks_str = request.GET.get('receipts', '')
    if receipt_pks_str and not receipts:
        pks = [int(x) for x in receipt_pks_str.split(',') if x.strip().isdigit()]
        receipts = list(
            Payment.objects.filter(pk__in=pks)
            .select_related('student_fee__fee_structure__fee_type')
            .order_by('pk')
        )

    return render(request, 'fees/fee_collection.html', {
        'query':              query,
        'students':           students,
        'student':            student,
        'dues':               dues,
        'receipts':           receipts,
        'payment_methods':    Payment.PAYMENT_METHODS,
        'today':              timezone.localdate().isoformat(),
        'browse_data_json':   _json.dumps(browse_data),
        'browse_div_id':      browse_div_id,
        'browse_grade_id':    browse_grade_id,
        'browse_section_id':  browse_section_id,
        'all_divisions':      all_divisions,
        'all_fee_types':      FeeType.objects.order_by('category', 'name'),
    })


# ════════════════════════════════════════════════════════════════
#  ADHOC / INDIVIDUAL FEE CHARGE
# ════════════════════════════════════════════════════════════════

@login_required
@role_required(*_ACCOUNTANT)
@require_POST
def charge_adhoc_fee(request):
    """
    Charge a one-off fee to a single student that is NOT part of their
    grade's fee structure (e.g. Library card, replacement ID, etc.).

    Strategy: get-or-create a sentinel Division/Grade/FeeStructure so that
    StudentFee always has a valid fee_structure FK — no model changes needed.
    """
    student_pk = request.POST.get('student_id')
    student = get_object_or_404(
        Student.objects.select_related('grade', 'section', 'division', 'academic_year'),
        pk=student_pk,
    )

    fee_type_pk = request.POST.get('adhoc_fee_type')
    try:
        fee_type = FeeType.objects.get(pk=fee_type_pk)
    except FeeType.DoesNotExist:
        messages.error(request, "Invalid fee type selected.")
        return redirect(f"{request.build_absolute_uri('/fees/collection/')}?student_id={student_pk}")

    raw_amount = request.POST.get('adhoc_amount', '').strip()
    try:
        amount = Decimal(raw_amount)
        if amount <= 0:
            raise ValueError
    except Exception:
        messages.error(request, "Enter a valid amount greater than 0.")
        return redirect(f"/fees/collection/?student_id={student_pk}")

    raw_pct = request.POST.get('adhoc_discount_pct', '').strip()
    try:
        discount_pct = Decimal(raw_pct) if raw_pct else Decimal('0')
    except Exception:
        discount_pct = Decimal('0')
    discount = (discount_pct / 100 * amount).quantize(Decimal('0.01'))
    discount_note = request.POST.get('adhoc_discount_note', '').strip()

    raw_due = request.POST.get('adhoc_due_date', '').strip()
    try:
        from datetime import date as _date
        due_date = _date.fromisoformat(raw_due) if raw_due else timezone.localdate()
    except ValueError:
        due_date = timezone.localdate()

    academic_year = student.academic_year
    if not academic_year:
        messages.error(request, "Student has no academic year assigned — cannot charge ad-hoc fee.")
        return redirect(f"/fees/collection/?student_id={student_pk}")

    # ── Sentinel objects (get-or-create) ────────────────────────
    # Use name='ADHOC' — Django doesn't enforce choices at the DB level
    # is_active=False keeps it hidden from all regular Division dropdowns
    sentinel_div, _ = Division.objects.get_or_create(
        name='ADHOC',
        defaults={'curriculum_type': 'ADHOC', 'is_active': False},
    )
    sentinel_grade, _ = Grade.objects.get_or_create(
        name='Ad-hoc Charges',
        division=sentinel_div,
        defaults={'order': 9999},
    )
    adhoc_structure, _ = FeeStructure.objects.get_or_create(
        academic_year=academic_year,
        grade=sentinel_grade,
        defaults={'name': 'Ad-hoc / Individual Charges'},
    )
    adhoc_item, _ = FeeStructureItem.objects.get_or_create(
        structure=adhoc_structure,
        fee_type=fee_type,
        defaults={'amount': amount},
    )

    # ── Create StudentFee (prevent duplicates) ───────────────────
    sf, created = StudentFee.objects.get_or_create(
        student=student,
        fee_structure=adhoc_item,
        defaults={
            'amount':        amount,
            'discount':      discount,
            'discount_note': discount_note,
            'due_date':      due_date,
            'assigned_by':   request.user,
        },
    )
    if not created:
        messages.warning(
            request,
            f"{fee_type.name} is already in this student's fee list. "
            "Select and pay it from the fees table below."
        )
    else:
        messages.success(
            request,
            f"'{fee_type.name}' (SAR {sf.net_amount:,.2f}) added to fee list — "
            f"select it below and submit payment."
        )

    return redirect(f"/fees/collection/?student_id={student_pk}#fees-section")


# ════════════════════════════════════════════════════════════════
#  RECEIPT (printable)
# ════════════════════════════════════════════════════════════════

@login_required
@role_required(*_ACCOUNTANT)
def receipt_print(request, payment_pk):
    payment = get_object_or_404(
        Payment.objects.select_related(
            'student_fee__student', 'student_fee__fee_structure__fee_type',
            'student_fee__student__grade', 'student_fee__student__section',
            'student_fee__student__division',
            'collected_by',
        ),
        pk=payment_pk,
    )

    # ── VAT breakdown for the paid amount ──────────────────────
    fee      = payment.student_fee
    student  = fee.student
    fee_type = fee.fee_structure.fee_type
    vat_rate = fee_type.vat_rate_for(student.is_saudi)  # 0 or Decimal('0.15')

    paid = payment.paid_amount
    if vat_rate > 0:
        paid_before_vat = (paid / (1 + vat_rate)).quantize(Decimal('0.01'))
        paid_vat        = (paid - paid_before_vat).quantize(Decimal('0.01'))
    else:
        paid_before_vat = paid
        paid_vat        = Decimal('0.00')

    vat_pct = int(vat_rate * 100)  # 0 or 15

    return render(request, 'fees/receipt_print.html', {
        'payment':        payment,
        'paid_before_vat': paid_before_vat,
        'paid_vat':        paid_vat,
        'vat_pct':         vat_pct,
    })


# ════════════════════════════════════════════════════════════════
#  COMBINED RECEIPT  (all payments in one transaction session)
# ════════════════════════════════════════════════════════════════

@login_required
@role_required(*_ACCOUNTANT)
def combined_receipt(request):
    """
    A single-page receipt covering multiple payments made in one session.
    URL: /fees/combined-receipt/?pks=1,2,3
    Shows: what was paid now + all remaining outstanding fees for the student.
    """
    pks_str = request.GET.get('pks', '')
    pks = [int(x) for x in pks_str.split(',') if x.strip().isdigit()]
    if not pks:
        return redirect('fees:collection')

    payments = list(
        Payment.objects.filter(pk__in=pks)
        .select_related(
            'student_fee__student',
            'student_fee__student__grade',
            'student_fee__student__section',
            'student_fee__student__division',
            'student_fee__fee_structure__fee_type',
            'collected_by',
        )
        .order_by('pk')
    )
    if not payments:
        return redirect('fees:collection')

    student = payments[0].student_fee.student

    # Build paid line items with VAT breakdown
    paid_lines = []
    total_paid = Decimal('0.00')
    total_vat  = Decimal('0.00')
    for p in payments:
        fee      = p.student_fee
        fee_type = fee.fee_structure.fee_type
        vat_rate = fee_type.vat_rate_for(student.is_saudi)
        paid     = p.paid_amount
        if vat_rate > 0:
            net = (paid / (1 + vat_rate)).quantize(Decimal('0.01'))
            vat = (paid - net).quantize(Decimal('0.01'))
        else:
            net = paid
            vat = Decimal('0.00')
        total_paid += paid
        total_vat  += vat
        paid_lines.append({
            'description': fee_type.name,
            'gross':       fee.amount,
            'discount':    fee.discount,
            'net':         net,
            'vat_pct':     int(vat_rate * 100),
            'vat':         vat,
            'paid':        paid,
            'note':        p.notes or '',
        })

    total_net_before_vat = (total_paid - total_vat).quantize(Decimal('0.01'))

    # Outstanding fees (exclude ADHOC, exclude fully paid, exclude fees just paid)
    paid_fee_pks = {p.student_fee_id for p in payments}
    outstanding = (
        StudentFee.objects
        .filter(student=student)
        .exclude(status='PAID')
        .exclude(status='WAIVED')
        .exclude(pk__in=paid_fee_pks)
        .select_related('fee_structure__fee_type',
                        'fee_structure__structure__grade__division')
        .order_by('due_date')
    )
    # Exclude ADHOC division items
    outstanding = [
        f for f in outstanding
        if f.fee_structure.structure.grade.division.name != 'ADHOC'
    ]
    total_outstanding = sum(f.balance for f in outstanding)

    # Use first payment's metadata for header info
    first = payments[0]

    return render(request, 'fees/combined_receipt.html', {
        'student':              student,
        'payments':             payments,
        'paid_lines':           paid_lines,
        'total_paid':           total_paid,
        'total_vat':            total_vat,
        'total_net_before_vat': total_net_before_vat,
        'outstanding':          outstanding,
        'total_outstanding':    total_outstanding,
        'payment_date':         first.payment_date,
        'payment_method':       first.get_payment_method_display(),
        'transaction_ref':      first.transaction_ref,
        'collected_by':         first.collected_by,
        'receipt_numbers':      ', '.join(p.receipt_number for p in payments),
    })


# ════════════════════════════════════════════════════════════════
#  STUDENT FEE EDIT (discount / status)
# ════════════════════════════════════════════════════════════════

@login_required
@role_required(*_ACCOUNTANT)
def student_fee_edit(request, pk):
    fee  = get_object_or_404(StudentFee.objects.select_related(
        'student', 'fee_structure__fee_type'), pk=pk)
    form = StudentFeeEditForm(request.POST or None, instance=fee)
    if form.is_valid():
        form.save()
        messages.success(request, "Fee updated.")
        return redirect(f"{request.path}?saved=1")
    return render(request, 'fees/student_fee_edit.html', {
        'fee': fee, 'form': form,
    })


# ════════════════════════════════════════════════════════════════
#  OUTSTANDING FEES REPORT
# ════════════════════════════════════════════════════════════════

@login_required
@role_required(*_ACCOUNTANT)
def outstanding_report(request):
    form = FeeReportFilterForm(request.GET or None)
    qs   = StudentFee.objects.select_related(
        'student', 'student__grade', 'student__section',
        'fee_structure__fee_type', 'fee_structure__structure__academic_year',
    )

    if form.is_valid() or request.GET:
        data = form.cleaned_data if form.is_valid() else {}

        year    = data.get('academic_year') or (
            AcademicYear.objects.filter(is_current=True).first())
        div     = data.get('division')
        grade   = data.get('grade')
        section = data.get('section')
        status  = data.get('status')
        ftype   = data.get('fee_type')

        if year:
            qs = qs.filter(fee_structure__structure__academic_year=year)
        if div:
            qs = qs.filter(student__division=div)
        if grade:
            qs = qs.filter(student__grade=grade)
        if section:
            qs = qs.filter(student__section=section)
        if status:
            qs = qs.filter(status=status)
        if ftype:
            qs = qs.filter(fee_structure__fee_type=ftype)
        as_of = data.get('as_of_date')
        if as_of:
            qs = qs.filter(due_date__lte=as_of)

    qs = qs.order_by('student__grade', 'student__section', 'student__full_name', 'due_date')

    # Totals
    totals = qs.aggregate(
        net=Sum('net_amount'),
    )
    paid_total = sum(f.amount_paid for f in qs)

    # Export CSV
    if request.GET.get('export') == 'csv':
        return _export_outstanding_csv(qs)

    return render(request, 'fees/outstanding_report.html', {
        'form':          form,
        'fees':          qs[:500],
        'net_total':     totals['net'] or 0,
        'paid_total':    paid_total,
        'balance_total': (totals['net'] or 0) - paid_total,
    })


def _export_outstanding_csv(qs):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="outstanding_fees.csv"'
    response.write('\ufeff')
    writer = csv.writer(response)
    writer.writerow(['Student ID', 'Name', 'Grade', 'Section', 'Fee Type',
                     'Net Amount', 'Paid', 'Balance', 'Due Date', 'Status'])
    for f in qs:
        writer.writerow([
            f.student.student_id,
            f.student.full_name,
            f.student.grade,
            f.student.section,
            f.fee_structure.fee_type.name,
            f.net_amount,
            f.amount_paid,
            f.balance,
            f.due_date,
            f.get_status_display(),
        ])
    return response


# ════════════════════════════════════════════════════════════════
#  STUDENT LEDGER
# ════════════════════════════════════════════════════════════════

@login_required
@role_required(*_ACCOUNTANT)
def student_ledger(request, student_pk):
    student = get_object_or_404(
        Student.objects.select_related('grade', 'section', 'division', 'academic_year'),
        pk=student_pk,
    )
    fees = StudentFee.objects.filter(student=student).select_related(
        'fee_structure__fee_type', 'fee_structure__structure__academic_year',
    ).prefetch_related('payments').order_by('fee_structure__structure__academic_year', 'due_date')

    total_net    = fees.aggregate(s=Sum('net_amount'))['s'] or Decimal('0')
    total_paid   = sum(f.amount_paid for f in fees)
    total_balance = total_net - total_paid

    invoices = TaxInvoice.objects.filter(student=student).order_by('-date')

    return render(request, 'fees/student_ledger.html', {
        'student':       student,
        'fees':          fees,
        'total_net':     total_net,
        'total_paid':    total_paid,
        'total_balance': total_balance,
        'invoices':      invoices,
    })


# ════════════════════════════════════════════════════════════════
#  DEFAULTERS LIST  (overdue fees, filterable by date)
# ════════════════════════════════════════════════════════════════

@login_required
@role_required(*_ACCOUNTANT)
def defaulters_list(request):
    filter_form = DefaultersFilterForm(request.GET or None)
    as_of       = timezone.localdate()
    grade_f     = None
    division_f  = None

    if filter_form.is_valid():
        as_of      = filter_form.cleaned_data.get('as_of_date') or as_of
        grade_f    = filter_form.cleaned_data.get('grade')
        division_f = filter_form.cleaned_data.get('division')

    fees = StudentFee.objects.filter(
        due_date__lte=as_of,
    ).exclude(
        status__in=['PAID', 'WAIVED'],
    ).select_related(
        'student', 'student__grade', 'student__section', 'student__division',
        'fee_structure__fee_type',
    )

    if grade_f:
        fees = fees.filter(student__grade=grade_f)
    if division_f:
        fees = fees.filter(student__division=division_f)

    fees = fees.order_by('due_date', 'student__full_name')

    # Mark overdue on the fly
    pks_to_mark = [f.pk for f in fees if f.status != 'OVERDUE']
    if pks_to_mark:
        StudentFee.objects.filter(pk__in=pks_to_mark).update(status='OVERDUE')

    total_overdue = fees.aggregate(s=Sum('net_amount'))['s'] or 0

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = (
            f'attachment; filename="defaulters_{as_of}.csv"'
        )
        response.write('\ufeff')
        writer = csv.writer(response)
        writer.writerow(['Student ID', 'Name', 'Grade', 'Section',
                         'Fee Type', 'Net Amount', 'Paid', 'Balance', 'Due Date', 'Days Overdue'])
        for f in fees:
            writer.writerow([
                f.student.student_id, f.student.full_name,
                f.student.grade, f.student.section,
                f.fee_structure.fee_type.name,
                f.net_amount, f.amount_paid, f.balance,
                f.due_date, (as_of - f.due_date).days,
            ])
        return response

    return render(request, 'fees/defaulters_list.html', {
        'fees':          fees,
        'total_overdue': total_overdue,
        'as_of':         as_of,
        'filter_form':   filter_form,
    })


# ════════════════════════════════════════════════════════════════
#  ZATCA TAX INVOICE
# ════════════════════════════════════════════════════════════════

@login_required
@role_required(*_ACCOUNTANT)
def invoice_list(request):
    student_q = request.GET.get('student', '').strip()
    qs = TaxInvoice.objects.select_related('student', 'created_by')
    if student_q:
        if student_q.isdigit():
            qs = qs.filter(student_id=student_q)
        else:
            qs = qs.filter(
                Q(student__full_name__icontains=student_q) |
                Q(student__arabic_name__icontains=student_q) |
                Q(student__student_id__icontains=student_q)
            )
    return render(request, 'fees/invoice_list.html', {
        'invoices':   qs.distinct()[:200],
        'student_pk': student_q,
    })


@login_required
@role_required(*_ACCOUNTANT)
def generate_invoice(request, student_pk):
    """
    Generate a ZATCA-compliant simplified tax invoice for a student
    covering all PAID fees in the current academic year (not yet invoiced).
    """
    student = get_object_or_404(Student, pk=student_pk)

    # Collect paid fees that are taxable
    paid_fees = StudentFee.objects.filter(
        student=student,
        status='PAID',
    ).select_related('fee_structure__fee_type')

    if not paid_fees.exists():
        messages.warning(request, "No paid fees found for this student.")
        return redirect('fees:student_ledger', student_pk=student_pk)

    subtotal   = Decimal('0')
    tax_total  = Decimal('0')
    line_items = []
    for f in paid_fees:
        base = f.amount - f.discount
        if base < 0:
            base = Decimal('0')
        rate = f.fee_structure.fee_type.vat_rate_for(student.is_saudi)
        tax  = (base * rate).quantize(Decimal('0.01'))
        subtotal  += base
        tax_total += tax
        line_items.append({
            'description':    f.fee_structure.fee_type.name,
            'qty':            1,
            'gross_amount':   float(f.amount),
            'discount':       float(f.discount),
            'net_before_vat': float(base),
            'vat_rate':       int(rate * 100),
            'vat':            float(tax),
            'total':          float(base + tax),
        })

    invoice = TaxInvoice.objects.create(
        student    = student,
        subtotal   = subtotal,
        tax_amount = tax_total,
        total      = subtotal + tax_total,
        status     = TaxInvoice.ISSUED,
        created_by = request.user,
        line_items_json = line_items,
    )
    messages.success(request, f"Invoice {invoice.invoice_number} generated.")
    return redirect('fees:invoice_print', pk=invoice.pk)


@login_required
@role_required(*_ACCOUNTANT)
def invoice_print(request, pk):
    invoice = get_object_or_404(
        TaxInvoice.objects.select_related('student', 'student__grade',
                                          'student__section', 'created_by'),
        pk=pk,
    )
    return render(request, 'fees/invoice_print.html', {
        'invoice':    invoice,
        'line_items': invoice.line_items_json or [],
    })


# ════════════════════════════════════════════════════════════════
#  PAYROLL
# ════════════════════════════════════════════════════════════════

@login_required
@role_required(*_ADMIN)
def payroll_list(request):
    form      = SalaryMonthFilterForm(request.GET or None)
    month_str = request.GET.get('month')
    salaries  = Salary.objects.select_related('staff').order_by('-month', 'staff__full_name')

    selected_month = None
    if month_str:
        try:
            # month input gives 'YYYY-MM'; convert to date
            selected_month = date.fromisoformat(month_str + '-01')
            salaries = salaries.filter(month=selected_month)
        except ValueError:
            pass

    total_net    = salaries.aggregate(s=Sum('net_salary'))['s'] or 0
    paid_count   = salaries.filter(is_paid=True).count()
    total_count  = salaries.count()
    unpaid_net   = salaries.filter(is_paid=False).aggregate(
        s=Sum('net_salary'))['s'] or 0

    # CSV export for bank upload
    if request.GET.get('export') == 'csv':
        return _export_payroll_csv(salaries, selected_month)

    return render(request, 'fees/payroll_list.html', {
        'salaries':    salaries,
        'form':        form,
        'total_net':   total_net,
        'paid_count':  paid_count,
        'total_count': total_count,
        'unpaid_net':  unpaid_net,
        'month_str':   month_str or '',
    })


def _export_payroll_csv(salaries, month):
    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    label    = month.strftime('%Y-%m') if month else 'all'
    response['Content-Disposition'] = f'attachment; filename="payroll_{label}.csv"'
    response.write('\ufeff')
    writer = csv.writer(response)
    writer.writerow(['Employee Name', 'Username', 'IBAN / Bank Ref', 'Month',
                     'Basic', 'Housing', 'Transport', 'Other Allow.',
                     'Deductions', 'Net Salary', 'Paid?'])
    for sal in salaries:
        name = sal.staff.full_name or sal.staff.username
        writer.writerow([
            name, sal.staff.username, sal.bank_ref,
            sal.month.strftime('%Y-%m'),
            sal.basic, sal.housing, sal.transport,
            sal.other_allowances, sal.deductions,
            sal.net_salary, 'Yes' if sal.is_paid else 'No',
        ])
    return response


@login_required
@role_required(*_ADMIN)
def salary_form(request, pk=None):
    instance = get_object_or_404(Salary, pk=pk) if pk else None
    form     = SalaryForm(request.POST or None, instance=instance)
    if form.is_valid():
        obj = form.save(commit=False)
        if not instance:
            obj.created_by = request.user
        obj.save()
        messages.success(request, "Salary record saved.")
        return redirect('fees:payroll_list')
    return render(request, 'fees/salary_form.html', {
        'form': form, 'title': 'Edit Salary' if instance else 'Add Salary',
        'instance': instance,
    })


@login_required
@role_required(*_ADMIN)
@require_POST
def salary_delete(request, pk):
    get_object_or_404(Salary, pk=pk).delete()
    messages.success(request, "Salary record deleted.")
    return redirect('fees:payroll_list')


@login_required
@role_required(*_ADMIN)
@require_POST
def mark_salary_paid(request, pk):
    sal          = get_object_or_404(Salary, pk=pk)
    sal.is_paid  = True
    sal.paid_date = timezone.localdate()
    sal.bank_ref  = request.POST.get('bank_ref', sal.bank_ref)
    sal.save()
    messages.success(request, f"Salary marked as paid for {sal.staff.full_name or sal.staff.username}.")
    return redirect('fees:payroll_list')


# ════════════════════════════════════════════════════════════════
#  FEES DASHBOARD
# ════════════════════════════════════════════════════════════════

@login_required
@role_required(*_ACCOUNTANT)
def fees_dashboard(request):
    today  = timezone.localdate()
    year   = AcademicYear.objects.filter(is_current=True).first()

    overdue_count  = StudentFee.objects.filter(status='OVERDUE').count()
    paid_today     = Payment.objects.filter(payment_date=today).aggregate(
        s=Sum('paid_amount'))['s'] or 0
    paid_month     = Payment.objects.filter(
        payment_date__year=today.year,
        payment_date__month=today.month,
    ).aggregate(s=Sum('paid_amount'))['s'] or 0

    total_assigned = StudentFee.objects.aggregate(s=Sum('net_amount'))['s'] or 0
    total_collected = Payment.objects.aggregate(s=Sum('paid_amount'))['s'] or 0

    recent_payments = Payment.objects.select_related(
        'student_fee__student', 'student_fee__fee_structure__fee_type',
        'collected_by',
    ).order_by('-payment_date', '-id')[:8]

    return render(request, 'fees/dashboard.html', {
        'overdue_count':   overdue_count,
        'paid_today':      paid_today,
        'paid_month':      paid_month,
        'total_assigned':  total_assigned,
        'total_collected': total_collected,
        'collection_pct':  round(float(total_collected) / float(total_assigned) * 100, 1)
                           if total_assigned else 0,
        'recent_payments': recent_payments,
        'year':            year,
        'actions': [
            ('Collect Payment',      '/fees/collection/',                   '💳', 'primary'),
            ('Fee Structures',       '/fees/structures/',                   '🗂️',  'slate'),
            ('Bulk Assign Fees',     '/fees/assign/',                       '📌', 'slate'),
            ('Outstanding Report',   '/fees/outstanding/',                  '📋', 'slate'),
            ('Defaulters List',      '/fees/defaulters/',                   '⚠️',  'red'),
            ('Tax Invoices',         '/fees/invoices/',                     '🧾', 'slate'),
            ('Payroll',              '/fees/payroll/',                      '💼', 'slate'),
            ('Fee Types',            '/fees/fee-types/',                    '🏷️',  'slate'),
        ],
    })


# ════════════════════════════════════════════════════════════════
#  MANUAL TAX INVOICE ENTRY
#  Handles: Cash Collection, Reservation Seat, Entrance Exam,
#           Tax Credit Note, Custom items
# ════════════════════════════════════════════════════════════════

@login_required
@role_required(*_ACCOUNTANT)
def manual_invoice(request, student_pk):
    """
    Create a manual tax invoice (or credit note) for a student
    with arbitrary line items — used for cash collection, reservation
    seat, entrance exam, discounts, etc.
    """
    student     = get_object_or_404(Student, pk=student_pk)
    header_form = ManualInvoiceHeaderForm(request.POST or None)

    # Build dynamic line-item formset from POST
    line_count = int(request.POST.get('line_count', 1))
    line_forms = [ManualInvoiceLineForm(request.POST or None, prefix=f'line_{i}')
                  for i in range(line_count)]

    if request.method == 'POST' and header_form.is_valid() and all(f.is_valid() for f in line_forms):
        subtotal  = Decimal('0')
        tax_total = Decimal('0')
        items     = []

        for lf in line_forms:
            d   = lf.cleaned_data
            amt = d['amount']
            if d.get('is_credit'):
                amt = -amt
            # Apply Saudi zero-rating: tuition/books are 0% for Saudi students
            effective_taxable = d.get('is_taxable', False)
            if effective_taxable and student.is_saudi:
                desc_lower = d['description'].lower()
                if any(kw in desc_lower for kw in ('tuition', 'رسوم دراسية', 'book', 'كتاب')):
                    effective_taxable = False
            tax = (amt * Decimal('0.15')).quantize(Decimal('0.01')) if effective_taxable else Decimal('0')
            subtotal  += amt
            tax_total += tax
            items.append({
                'description':    d['description'],
                'qty':            1,
                'gross_amount':   float(abs(amt)),
                'discount':       0,
                'net_before_vat': float(amt),
                'vat_rate':       15 if effective_taxable else 0,
                'vat':            float(tax),
                'total':          float(amt + tax),
                'is_credit':      d.get('is_credit', False),
            })

        hd           = header_form.cleaned_data
        inv_type     = hd['invoice_type']
        inv_status   = TaxInvoice.ISSUED
        if inv_type == TaxInvoice.INVOICE_TYPE_CREDIT_NOTE:
            inv_status = TaxInvoice.CREDIT_NOTE

        invoice = TaxInvoice.objects.create(
            student         = student,
            date            = hd['date'],
            subtotal        = subtotal,
            tax_amount      = tax_total,
            total           = subtotal + tax_total,
            status          = inv_status,
            invoice_type    = inv_type,
            notes           = hd.get('notes', ''),
            created_by      = request.user,
            line_items_json = items,
        )
        messages.success(request, f"Invoice {invoice.invoice_number} created.")
        return redirect('fees:invoice_print', pk=invoice.pk)

    return render(request, 'fees/manual_invoice_form.html', {
        'student':     student,
        'header_form': header_form,
        'line_forms':  line_forms,
        'line_count':  line_count,
        'is_saudi':    student.is_saudi,
    })


# ════════════════════════════════════════════════════════════════
#  BANK VERIFICATION  (mark payment verified against bank stmt)
# ════════════════════════════════════════════════════════════════

@login_required
@role_required(*_ACCOUNTANT)
@require_POST
def bank_verify_payment(request, payment_pk):
    payment = get_object_or_404(Payment, pk=payment_pk)
    payment.bank_verified    = True
    payment.bank_verified_at = timezone.localdate()
    # Allow updating bank ref from POST
    ref = request.POST.get('bank_ref', '').strip()
    if ref:
        payment.transaction_ref = ref
    payment.save(update_fields=['bank_verified', 'bank_verified_at', 'transaction_ref'])
    messages.success(request, f"Receipt {payment.receipt_number} marked as bank-verified.")
    return redirect('fees:receipt_print', payment_pk=payment_pk)


# ════════════════════════════════════════════════════════════════
#  TUITION FEE CONFIG  (complete structured fee schedule)
# ════════════════════════════════════════════════════════════════

@login_required
@role_required(*_ACCOUNTANT)
def tuition_config_list(request):
    """List all tuition fee configurations with filter support."""
    filter_form = TuitionConfigFilterForm(request.GET or None)
    qs = TuitionFeeConfig.objects.select_related(
        'academic_year', 'division', 'grade',
    ).prefetch_related('installments')

    if filter_form.is_valid():
        year    = filter_form.cleaned_data.get('academic_year')
        div     = filter_form.cleaned_data.get('division')
        stype   = filter_form.cleaned_data.get('structure_type')
        if year:
            qs = qs.filter(academic_year=year)
        if div:
            qs = qs.filter(division=div)
        if stype:
            qs = qs.filter(structure_type=stype)

    return render(request, 'fees/tuition_config_list.html', {
        'configs':     qs,
        'filter_form': filter_form,
    })


@login_required
@role_required(*_ADMIN)
def tuition_config_form(request, pk=None):
    """Create or edit a tuition fee configuration with inline installments."""
    instance = get_object_or_404(TuitionFeeConfig, pk=pk) if pk else None
    form     = TuitionFeeConfigForm(request.POST or None, instance=instance)

    if instance:
        formset = TuitionInstallmentFormSet(
            request.POST or None, instance=instance)
    else:
        formset = TuitionInstallmentFormSet(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        config  = form.save(commit=False)
        formset = TuitionInstallmentFormSet(request.POST, instance=config)
        if formset.is_valid():
            config.save()
            formset.save()
            # Post-save validation warning (non-blocking)
            errors = config.validate_installments()
            if errors:
                for e in errors:
                    messages.warning(request, f"Validation: {e}")
            else:
                messages.success(request, "Tuition fee configuration saved successfully.")
            return redirect('fees:tuition_config_detail', pk=config.pk)

    return render(request, 'fees/tuition_config_form.html', {
        'form':     form,
        'formset':  formset,
        'title':    'Edit Tuition Fee Config' if instance else 'New Tuition Fee Config',
        'instance': instance,
    })


@login_required
@role_required(*_ACCOUNTANT)
def tuition_config_detail(request, pk):
    """Full structured fee table for a single configuration."""
    config = get_object_or_404(
        TuitionFeeConfig.objects.select_related(
            'academic_year', 'division', 'grade',
            'from_academic_year', 'to_academic_year',
        ).prefetch_related('installments'),
        pk=pk,
    )
    installments = sorted(
        config.installments.all(),
        key=lambda i: TuitionInstallment.INSTALLMENT_ORDER.get(i.installment_type, 99),
    )
    validation_errors = config.validate_installments()
    return render(request, 'fees/tuition_config_detail.html', {
        'config':            config,
        'installments':      installments,
        'validation_errors': validation_errors,
    })


@login_required
@role_required(*_ADMIN)
@require_POST
def tuition_config_delete(request, pk):
    config = get_object_or_404(TuitionFeeConfig, pk=pk)
    config.delete()
    messages.success(request, "Tuition fee configuration deleted.")
    return redirect('fees:tuition_config_list')


@login_required
@role_required(*_ACCOUNTANT)
def tuition_config_print(request, pk):
    """Print-optimised view of a full tuition fee schedule."""
    config = get_object_or_404(
        TuitionFeeConfig.objects.select_related(
            'academic_year', 'division', 'grade',
            'from_academic_year', 'to_academic_year',
        ).prefetch_related('installments'),
        pk=pk,
    )
    installments = sorted(
        config.installments.all(),
        key=lambda i: TuitionInstallment.INSTALLMENT_ORDER.get(i.installment_type, 99),
    )
    return render(request, 'fees/tuition_config_print.html', {
        'config':       config,
        'installments': installments,
    })


@login_required
@role_required(*_ACCOUNTANT)
def tuition_config_export_csv(request):
    """Export all (filtered) tuition configurations to CSV."""
    filter_form = TuitionConfigFilterForm(request.GET or None)
    qs = TuitionFeeConfig.objects.select_related(
        'academic_year', 'division', 'grade',
    ).prefetch_related('installments')

    if filter_form.is_valid():
        year  = filter_form.cleaned_data.get('academic_year')
        div   = filter_form.cleaned_data.get('division')
        stype = filter_form.cleaned_data.get('structure_type')
        if year:
            qs = qs.filter(academic_year=year)
        if div:
            qs = qs.filter(division=div)
        if stype:
            qs = qs.filter(structure_type=stype)

    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="tuition_fee_structure.csv"'
    response.write('\ufeff')
    writer = csv.writer(response)
    writer.writerow([
        'Academic Year', 'Division', 'Grade', 'Structure Type',
        'No. of Payments', 'Includes Books',
        'Entrance Exam Fee (SAR)', 'Registration Fee (SAR)',
        'Reservation / Down Payment (SAR)',
        'Gross Tuition (SAR)',
        'Group Discount Enabled', 'Group Discount (%)',
        'Group Discount Amount (SAR)',
        'Net Tuition – Saudi (SAR)',
        'VAT Rate (%)', 'VAT Amount – Non-Saudi (SAR)',
        'Final Tuition – Non-Saudi (SAR)',
        'Reservation Installment (SAR)',
        '1st Installment (SAR)',
        '2nd Installment (SAR)',
        '3rd Installment (SAR)',
        'Notes',
    ])
    for cfg in qs:
        insts = {i.installment_type: i.amount for i in cfg.installments.all()}
        writer.writerow([
            str(cfg.academic_year),
            str(cfg.division),
            str(cfg.grade),
            cfg.get_structure_type_display(),
            cfg.num_payments,
            'Yes' if cfg.includes_books else 'No',
            cfg.entrance_exam_fee,
            cfg.registration_fee,
            cfg.reservation_fee,
            cfg.gross_tuition_fee,
            'Yes' if cfg.group_discount_enabled else 'No',
            cfg.group_discount_pct if cfg.group_discount_enabled else 0,
            cfg.group_discount_amount,
            cfg.net_tuition_fee,
            cfg.vat_pct,
            cfg.vat_amount_non_saudi,
            cfg.final_net_non_saudi,
            insts.get(TuitionInstallment.RESERVATION, ''),
            insts.get(TuitionInstallment.FIRST, ''),
            insts.get(TuitionInstallment.SECOND, ''),
            insts.get(TuitionInstallment.THIRD, ''),
            cfg.notes,
        ])
    return response


# ════════════════════════════════════════════════════════════════
#  PAYMENT PLAN  (installment schedule per student fee)
# ════════════════════════════════════════════════════════════════

@login_required
@role_required(*_ACCOUNTANT)
def setup_payment_plan(request, student_fee_pk):
    """
    Create or replace an installment plan for a StudentFee.
    GET  → show form.
    POST → validate & save plan installments.
    """
    sf = get_object_or_404(
        StudentFee.objects.select_related(
            'student', 'fee_structure', 'fee_structure__fee_type'),
        pk=student_fee_pk,
    )

    if sf.balance <= 0:
        messages.error(request, "This fee is already fully paid — no installment plan needed.")
        from django.urls import reverse
        return redirect(reverse('fees:collection') + f"?student_id={sf.student_id}")

    existing_plan = getattr(sf, 'payment_plan', None)

    if request.method == 'POST':
        count_str = request.POST.get('installment_count', '2')
        try:
            count = max(2, min(12, int(count_str)))
        except ValueError:
            count = 2

        amounts   = []
        due_dates = []
        errors    = []

        for i in range(1, count + 1):
            amt_raw = request.POST.get(f'inst_amount_{i}', '').strip()
            due_raw = request.POST.get(f'inst_due_{i}', '').strip()
            try:
                amt = Decimal(amt_raw)
                if amt <= 0:
                    raise ValueError
            except Exception:
                errors.append(f"Installment {i}: enter a valid amount.")
                amt = Decimal('0')
            try:
                due = date.fromisoformat(due_raw)
            except Exception:
                errors.append(f"Installment {i}: enter a valid due date.")
                due = timezone.localdate()
            amounts.append(amt)
            due_dates.append(due)

        total_inst = sum(amounts)
        if abs(total_inst - sf.balance) > Decimal('0.01'):
            errors.append(
                f"Installments total SAR {total_inst:,.2f} does not match "
                f"outstanding balance SAR {sf.balance:,.2f}."
            )

        if errors:
            for e in errors:
                messages.error(request, e)
        else:
            if existing_plan:
                existing_plan.delete()

            plan = PaymentPlan.objects.create(
                student_fee=sf,
                notes=request.POST.get('notes', '').strip(),
                created_by=request.user,
            )
            for idx, (amt, due) in enumerate(zip(amounts, due_dates), start=1):
                PaymentPlanInstallment.objects.create(
                    plan=plan,
                    installment_no=idx,
                    amount=amt,
                    due_date=due,
                )
            messages.success(
                request,
                f"Installment plan saved — {count} installments for "
                f"{sf.fee_structure.fee_type.name}."
            )
            from django.urls import reverse
            return redirect(reverse('fees:collection') + f"?student_id={sf.student_id}")

    from django.urls import reverse
    return render(request, 'fees/payment_plan_form.html', {
        'sf':            sf,
        'existing_plan': existing_plan,
        'back_url':      reverse('fees:collection') + f"?student_id={sf.student_id}",
    })


@login_required
@role_required(*_ACCOUNTANT)
def delete_payment_plan(request, plan_pk):
    """Delete an installment plan (POST only)."""
    plan = get_object_or_404(
        PaymentPlan.objects.select_related('student_fee__student'),
        pk=plan_pk,
    )
    student_id = plan.student_fee.student_id
    if request.method == 'POST':
        plan.delete()
        messages.success(request, "Installment plan deleted.")
    from django.urls import reverse
    return redirect(reverse('fees:collection') + f"?student_id={student_id}")


