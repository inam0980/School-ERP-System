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
from .models import FeeType, FeeStructure, StudentFee, Payment, TaxInvoice, Salary
from .forms import (
    FeeTypeForm, FeeStructureForm, BulkAssignFeeForm,
    StudentFeeEditForm, PaymentForm, FeeReportFilterForm,
    SalaryForm, SalaryMonthFilterForm,
    ManualInvoiceHeaderForm, ManualInvoiceLineForm, DefaultersFilterForm,
)

_ADMIN       = ('SUPER_ADMIN', 'ADMIN')
_ACCOUNTANT  = ('SUPER_ADMIN', 'ADMIN', 'ACCOUNTANT')
_STAFF_VIEW  = ('SUPER_ADMIN', 'ADMIN', 'ACCOUNTANT', 'STAFF')


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
        'academic_year', 'grade', 'division', 'fee_type'
    )
    if year_id:
        qs = qs.filter(academic_year_id=year_id)
    return render(request, 'fees/fee_structure_list.html', {
        'structures': qs,
        'years': AcademicYear.objects.all(),
        'active_year': year_id,
    })


@login_required
@role_required(*_ADMIN)
def fee_structure_form(request, pk=None):
    instance = get_object_or_404(FeeStructure, pk=pk) if pk else None
    form     = FeeStructureForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        messages.success(request, "Fee structure saved.")
        return redirect('fees:fee_structure_list')
    return render(request, 'fees/fee_structure_form.html', {
        'form': form, 'title': 'Edit Structure' if instance else 'Add Fee Structure',
    })


@login_required
@role_required(*_ADMIN)
@require_POST
def fee_structure_delete(request, pk):
    get_object_or_404(FeeStructure, pk=pk).delete()
    messages.success(request, "Fee structure deleted.")
    return redirect('fees:fee_structure_list')


# ════════════════════════════════════════════════════════════════
#  BULK FEE ASSIGNMENT
# ════════════════════════════════════════════════════════════════

@login_required
@role_required(*_ACCOUNTANT)
def bulk_assign_fees(request):
    form    = BulkAssignFeeForm(request.POST or None)
    results = None

    if form.is_valid():
        structure     = form.cleaned_data['fee_structure']
        section       = form.cleaned_data.get('section')
        discount      = form.cleaned_data['discount']
        discount_note = form.cleaned_data.get('discount_note', '')

        students = Student.objects.filter(
            grade=structure.grade,
            is_active=True,
        )
        if section:
            students = students.filter(section=section)

        created = updated = skipped = 0
        for student in students:
            obj, created_flag = StudentFee.objects.get_or_create(
                student=student,
                fee_structure=structure,
                defaults={
                    'amount':        structure.amount,
                    'discount':      discount,
                    'discount_note': discount_note,
                    'due_date':      structure.due_date,
                    'assigned_by':   request.user,
                },
            )
            if created_flag:
                obj.save()          # triggers net_amount calc
                created += 1
            else:
                skipped += 1

        results = {'created': created, 'skipped': skipped}
        messages.success(
            request,
            f"Done — {created} fees created, {skipped} already existed."
        )

    return render(request, 'fees/bulk_assign.html', {
        'form': form, 'results': results,
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
    """
    query    = request.GET.get('q', '').strip()
    students = []
    student  = None
    dues     = []

    if query:
        students = Student.objects.filter(
            Q(full_name__icontains=query) |
            Q(student_id__icontains=query) |
            Q(arabic_name__icontains=query),
            is_active=True,
        ).select_related('grade', 'section')[:20]

    student_pk = request.GET.get('student_id') or request.POST.get('student_id')
    if student_pk:
        student = get_object_or_404(
            Student.objects.select_related('grade', 'section', 'division', 'academic_year'),
            pk=student_pk,
        )
        dues = list(
            StudentFee.objects.filter(student=student)
            .exclude(status__in=['WAIVED', 'PAID'])
            .select_related('fee_structure', 'fee_structure__fee_type')
            .order_by('due_date')
        )

    # ── MULTI-FEE POST ──────────────────────────────────────────
    receipts = []
    if request.method == 'POST' and student:
        selected_pks = request.POST.getlist('selected_fees')
        if not selected_pks:
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

            for pk in selected_pks:
                try:
                    fee = StudentFee.objects.select_related(
                        'fee_structure__fee_type').get(pk=pk, student=student)
                except StudentFee.DoesNotExist:
                    continue

                # Apply inline discount
                raw_disc = request.POST.get(f'discount_{pk}', '').strip()
                try:
                    disc = Decimal(raw_disc) if raw_disc else Decimal('0')
                except Exception:
                    disc = Decimal('0')
                if disc > 0:
                    fee.discount      = (fee.discount or Decimal('0')) + disc
                    fee.discount_note = request.POST.get(f'discount_note_{pk}', '').strip()
                    fee.save()          # recalculates net_amount

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
        'query':           query,
        'students':        students,
        'student':         student,
        'dues':            dues,
        'receipts':        receipts,
        'payment_methods': Payment.PAYMENT_METHODS,
        'today':           timezone.localdate().isoformat(),
    })


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
            'collected_by',
        ),
        pk=payment_pk,
    )
    return render(request, 'fees/receipt_print.html', {'payment': payment})


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
        'fee_structure__fee_type', 'fee_structure__academic_year',
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
            qs = qs.filter(fee_structure__academic_year=year)
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
        'fee_structure__fee_type', 'fee_structure__academic_year',
    ).prefetch_related('payments').order_by('fee_structure__academic_year', 'due_date')

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
    student_pk = request.GET.get('student')
    qs = TaxInvoice.objects.select_related('student', 'created_by')
    if student_pk:
        qs = qs.filter(student_id=student_pk)
    return render(request, 'fees/invoice_list.html', {
        'invoices':   qs[:200],
        'student_pk': student_pk,
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

