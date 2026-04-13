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
    Search student → show all outstanding fees → collect payment on one fee.
    GET with ?student_id=X shows the student's dues.
    POST with student_fee_id + payment data records the payment.
    """
    query      = request.GET.get('q', '').strip()
    students   = []
    student    = None
    dues       = []
    pay_form   = None
    selected_fee = None

    if query:
        students = Student.objects.filter(
            Q(full_name__icontains=query) |
            Q(student_id__icontains=query) |
            Q(arabic_name__icontains=query),
            is_active=True,
        ).select_related('grade', 'section')[:20]

    student_pk = request.GET.get('student_id') or request.POST.get('student_id')
    if student_pk:
        student = get_object_or_404(Student.objects.select_related(
            'grade', 'section', 'division', 'academic_year'), pk=student_pk)
        dues = StudentFee.objects.filter(
            student=student,
        ).exclude(status='WAIVED').select_related(
            'fee_structure', 'fee_structure__fee_type'
        ).order_by('due_date')

    # Which fee to pay?
    fee_pk = request.GET.get('fee_id') or request.POST.get('student_fee_id')
    if fee_pk:
        selected_fee = get_object_or_404(StudentFee.objects.select_related(
            'student', 'fee_structure__fee_type'), pk=fee_pk)

    if request.method == 'POST' and selected_fee:
        pay_form = PaymentForm(request.POST)
        if pay_form.is_valid():
            payment = pay_form.save(commit=False)
            payment.student_fee  = selected_fee
            payment.collected_by = request.user
            # Clamp to balance
            if payment.paid_amount > selected_fee.balance:
                payment.paid_amount = selected_fee.balance
            payment.save()
            messages.success(
                request,
                f"Payment of SAR {payment.paid_amount} recorded. Receipt: {payment.receipt_number}"
            )
            return redirect(
                f"{request.path}?student_id={student.pk}&receipt={payment.pk}"
            )
    else:
        if selected_fee:
            pay_form = PaymentForm(initial={'paid_amount': selected_fee.balance})

    receipt = None
    receipt_pk = request.GET.get('receipt')
    if receipt_pk:
        receipt = get_object_or_404(Payment.objects.select_related(
            'student_fee__student', 'student_fee__fee_structure__fee_type',
            'collected_by'), pk=receipt_pk)

    return render(request, 'fees/fee_collection.html', {
        'query':        query,
        'students':     students,
        'student':      student,
        'dues':         dues,
        'selected_fee': selected_fee,
        'pay_form':     pay_form,
        'receipt':      receipt,
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
#  DEFAULTERS LIST  (overdue > 30 days)
# ════════════════════════════════════════════════════════════════

@login_required
@role_required(*_ACCOUNTANT)
def defaulters_list(request):
    cutoff = timezone.localdate() - timedelta(days=30)
    fees   = StudentFee.objects.filter(
        due_date__lte=cutoff,
    ).exclude(
        status__in=['PAID', 'WAIVED'],
    ).select_related(
        'student', 'student__grade', 'student__section',
        'fee_structure__fee_type',
    ).order_by('due_date', 'student__full_name')

    # Refresh status on-the-fly
    for f in fees:
        if f.status != 'OVERDUE':
            f.status = 'OVERDUE'
            StudentFee.objects.filter(pk=f.pk).update(status='OVERDUE')

    total_overdue = fees.aggregate(s=Sum('net_amount'))['s'] or 0

    if request.GET.get('export') == 'csv':
        response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
        response['Content-Disposition'] = 'attachment; filename="defaulters.csv"'
        response.write('\ufeff')
        writer = csv.writer(response)
        writer.writerow(['Student ID', 'Name', 'Grade', 'Section',
                         'Fee Type', 'Net Amount', 'Paid', 'Balance', 'Due Date', 'Days Overdue'])
        today = timezone.localdate()
        for f in fees:
            writer.writerow([
                f.student.student_id, f.student.full_name,
                f.student.grade, f.student.section,
                f.fee_structure.fee_type.name,
                f.net_amount, f.amount_paid, f.balance,
                f.due_date, (today - f.due_date).days,
            ])
        return response

    return render(request, 'fees/defaulters_list.html', {
        'fees':          fees,
        'total_overdue': total_overdue,
        'cutoff':        cutoff,
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
        tax = (base * Decimal('0.15')).quantize(Decimal('0.01')) if f.fee_structure.fee_type.is_taxable else Decimal('0')
        subtotal  += base
        tax_total += tax
        line_items.append({
            'description': f.fee_structure.fee_type.name,
            'amount':      float(base),
            'is_taxable':  f.fee_structure.fee_type.is_taxable,
            'tax':         float(tax),
            'total':       float(base + tax),
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
    salaries  = Salary.objects.select_related('staff').order_by('-month', 'staff__first_name')

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
        name = sal.staff.get_full_name() or sal.staff.username
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
    messages.success(request, f"Salary marked as paid for {sal.staff.get_full_name() or sal.staff.username}.")
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
    })
