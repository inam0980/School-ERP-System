import uuid
from decimal import Decimal
from django.db import models
from django.conf import settings
from django.utils import timezone
from core.models import AcademicYear, Division, Grade, Section
from students.models import Student


# ════════════════════════════════════════════════════════════════
#  FEE TYPE
# ════════════════════════════════════════════════════════════════

class FeeType(models.Model):
    TUITION        = 'TUITION'
    TRANSPORT      = 'TRANSPORT'
    UNIFORM        = 'UNIFORM'
    BOOKS          = 'BOOKS'
    EXTRACURRICULAR = 'EXTRACURRICULAR'
    OTHER          = 'OTHER'

    FEE_CATEGORIES = [
        (TUITION,         'Tuition / رسوم دراسية'),
        (TRANSPORT,       'Transport / مواصلات'),
        (UNIFORM,         'Uniform / زي مدرسي'),
        (BOOKS,           'Books & Supplies / كتب ومستلزمات'),
        (EXTRACURRICULAR, 'Extracurricular / أنشطة'),
        (OTHER,           'Other / أخرى'),
    ]

    name        = models.CharField(max_length=100)
    category    = models.CharField(max_length=20, choices=FEE_CATEGORIES, default=OTHER)
    is_taxable  = models.BooleanField(default=False, help_text="Subject to 15% VAT (ZATCA)")
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


# ════════════════════════════════════════════════════════════════
#  FEE STRUCTURE  (per grade / division / year)
# ════════════════════════════════════════════════════════════════

class FeeStructure(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT,
                                      related_name='fee_structures')
    grade         = models.ForeignKey(Grade,        on_delete=models.PROTECT,
                                      related_name='fee_structures')
    division      = models.ForeignKey(Division,     on_delete=models.PROTECT,
                                      related_name='fee_structures')
    fee_type      = models.ForeignKey(FeeType,      on_delete=models.PROTECT,
                                      related_name='structures')
    amount        = models.DecimalField(max_digits=10, decimal_places=2)
    due_date      = models.DateField(help_text="Deadline for payment")
    frequency     = models.CharField(max_length=20, choices=[
        ('ONCE',      'One-time'),
        ('MONTHLY',   'Monthly'),
        ('TERM',      'Per Term'),
        ('ANNUAL',    'Annual'),
    ], default='ANNUAL')
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['academic_year', 'grade', 'division', 'fee_type']
        ordering = ['grade', 'fee_type']

    def __str__(self):
        return f"{self.fee_type.name} — {self.grade} ({self.academic_year}) — SAR {self.amount}"

    @property
    def tax_amount(self):
        if self.fee_type.is_taxable:
            return (self.amount * Decimal('0.15')).quantize(Decimal('0.01'))
        return Decimal('0.00')

    @property
    def gross_amount(self):
        return self.amount + self.tax_amount


# ════════════════════════════════════════════════════════════════
#  STUDENT FEE  (assigned instance per student)
# ════════════════════════════════════════════════════════════════

class StudentFee(models.Model):
    UNPAID   = 'UNPAID'
    PARTIAL  = 'PARTIAL'
    PAID     = 'PAID'
    OVERDUE  = 'OVERDUE'
    WAIVED   = 'WAIVED'

    STATUS_CHOICES = [
        (UNPAID,  'Unpaid / غير مدفوع'),
        (PARTIAL, 'Partial / مدفوع جزئيًا'),
        (PAID,    'Paid / مدفوع'),
        (OVERDUE, 'Overdue / متأخر'),
        (WAIVED,  'Waived / معفى'),
    ]

    student       = models.ForeignKey(Student,      on_delete=models.CASCADE,
                                      related_name='fees')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.PROTECT,
                                      related_name='student_fees')
    amount        = models.DecimalField(max_digits=10, decimal_places=2,
                                        help_text="Base amount (copied from structure)")
    discount      = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                        help_text="Discount in SAR")
    discount_note = models.CharField(max_length=200, blank=True)
    net_amount    = models.DecimalField(max_digits=10, decimal_places=2,
                                        help_text="amount − discount + tax")
    due_date      = models.DateField()
    status        = models.CharField(max_length=10, choices=STATUS_CHOICES, default=UNPAID)
    created_at    = models.DateTimeField(auto_now_add=True)
    assigned_by   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                      null=True, blank=True, related_name='fees_assigned')

    class Meta:
        unique_together = ['student', 'fee_structure']
        ordering = ['due_date', 'student']

    def __str__(self):
        return f"{self.student} — {self.fee_structure.fee_type.name} — {self.status}"

    def save(self, *args, **kwargs):
        # Net = amount – discount + VAT on (amount – discount)
        base = self.amount - self.discount
        if base < 0:
            base = Decimal('0.00')
        if self.fee_structure.fee_type.is_taxable:
            self.net_amount = (base * Decimal('1.15')).quantize(Decimal('0.01'))
        else:
            self.net_amount = base.quantize(Decimal('0.01'))
        super().save(*args, **kwargs)

    @property
    def amount_paid(self):
        return self.payments.aggregate(s=models.Sum('paid_amount'))['s'] or Decimal('0.00')

    @property
    def balance(self):
        return self.net_amount - self.amount_paid

    def refresh_status(self):
        paid = self.amount_paid
        if self.status == self.WAIVED:
            return
        if paid <= 0:
            self.status = self.OVERDUE if self.due_date < timezone.localdate() else self.UNPAID
        elif paid >= self.net_amount:
            self.status = self.PAID
        else:
            self.status = self.PARTIAL
        self.save(update_fields=['status'])


# ════════════════════════════════════════════════════════════════
#  PAYMENT
# ════════════════════════════════════════════════════════════════

def _receipt_number():
    return "RCP-" + str(uuid.uuid4().int)[:8].upper()


class Payment(models.Model):
    CASH    = 'CASH'
    BANK    = 'BANK'
    MADA    = 'MADA'
    ONLINE  = 'ONLINE'
    CHEQUE  = 'CHEQUE'

    PAYMENT_METHODS = [
        (CASH,   'Cash / نقدًا'),
        (BANK,   'Bank Transfer / تحويل بنكي'),
        (MADA,   'Mada / مدى'),
        (ONLINE, 'Online / إلكتروني'),
        (CHEQUE, 'Cheque / شيك'),
    ]

    student_fee    = models.ForeignKey(StudentFee, on_delete=models.CASCADE,
                                       related_name='payments')
    paid_amount    = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date   = models.DateField(default=timezone.localdate)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default=CASH)
    receipt_number = models.CharField(max_length=30, unique=True,
                                      default=_receipt_number, editable=False)
    transaction_ref = models.CharField(max_length=100, blank=True,
                                       help_text="Bank ref / cheque no.")
    notes          = models.TextField(blank=True)
    collected_by   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                       null=True, blank=True, related_name='payments_collected')

    class Meta:
        ordering = ['-payment_date', '-id']

    def __str__(self):
        return f"{self.receipt_number} — SAR {self.paid_amount}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update parent StudentFee status after every payment
        self.student_fee.refresh_status()


# ════════════════════════════════════════════════════════════════
#  TAX INVOICE  (ZATCA simplified e-invoice)
# ════════════════════════════════════════════════════════════════

def _invoice_number():
    ts  = timezone.now().strftime('%Y%m%d')
    uid = str(uuid.uuid4().int)[:5]
    return f"INV-{ts}-{uid}"


class TaxInvoice(models.Model):
    DRAFT   = 'DRAFT'
    ISSUED  = 'ISSUED'
    VOIDED  = 'VOIDED'

    STATUS_CHOICES = [
        (DRAFT,  'Draft'),
        (ISSUED, 'Issued'),
        (VOIDED, 'Voided'),
    ]

    student        = models.ForeignKey(Student, on_delete=models.PROTECT,
                                       related_name='invoices')
    invoice_number = models.CharField(max_length=40, unique=True,
                                      default=_invoice_number, editable=False)
    date           = models.DateField(default=timezone.localdate)
    subtotal       = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount     = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total          = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status         = models.CharField(max_length=10, choices=STATUS_CHOICES, default=DRAFT)
    notes          = models.TextField(blank=True)
    created_by     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                       null=True, blank=True, related_name='invoices_created')
    # Line items stored as JSON snapshot
    line_items_json = models.JSONField(default=list, blank=True)

    class Meta:
        ordering = ['-date', '-id']

    def __str__(self):
        return f"{self.invoice_number} — {self.student.full_name}"


# ════════════════════════════════════════════════════════════════
#  SALARY  (staff payroll)
# ════════════════════════════════════════════════════════════════

class Salary(models.Model):
    staff         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT,
                                      related_name='salaries',
                                      limit_choices_to={'role__in': ['TEACHER', 'ACCOUNTANT', 'STAFF', 'ADMIN']})
    month         = models.DateField(help_text="First day of the month (e.g. 2025-09-01)")
    basic         = models.DecimalField(max_digits=10, decimal_places=2)
    housing       = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                        verbose_name="Housing Allowance")
    transport     = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                        verbose_name="Transport Allowance")
    other_allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions    = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                        help_text="Absences / penalties")
    net_salary    = models.DecimalField(max_digits=10, decimal_places=2, editable=False,
                                        default=0)
    is_paid       = models.BooleanField(default=False)
    paid_date     = models.DateField(null=True, blank=True)
    bank_ref      = models.CharField(max_length=100, blank=True,
                                     verbose_name="Bank Transfer Ref")
    notes         = models.TextField(blank=True)
    created_by    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                      null=True, blank=True, related_name='salaries_created')

    class Meta:
        unique_together = ['staff', 'month']
        ordering = ['-month']

    def __str__(self):
        return f"{self.staff.get_full_name() or self.staff.username} — {self.month.strftime('%b %Y')} — SAR {self.net_salary}"

    def save(self, *args, **kwargs):
        allowances    = self.housing + self.transport + self.other_allowances
        self.net_salary = self.basic + allowances - self.deductions
        if self.net_salary < 0:
            self.net_salary = Decimal('0.00')
        super().save(*args, **kwargs)
