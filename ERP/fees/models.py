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
    TUITION          = 'TUITION'
    ADMISSION        = 'ADMISSION'
    REGISTRATION     = 'REGISTRATION'
    EXAMINATION      = 'EXAMINATION'
    TRANSPORT        = 'TRANSPORT'
    UNIFORM          = 'UNIFORM'
    BOOKS            = 'BOOKS'
    EXTRACURRICULAR  = 'EXTRACURRICULAR'
    LIBRARY          = 'LIBRARY'
    LABORATORY       = 'LABORATORY'
    SPORTS           = 'SPORTS'
    ANNUAL_FUNCTION  = 'ANNUAL_FUNCTION'
    DEVELOPMENT      = 'DEVELOPMENT'
    SMART_CLASS      = 'SMART_CLASS'
    ID_CARD          = 'ID_CARD'
    SECURITY_DEPOSIT = 'SECURITY_DEPOSIT'
    HOSTEL           = 'HOSTEL'
    MESS             = 'MESS'
    LATE_FEE         = 'LATE_FEE'
    RESERVATION      = 'RESERVATION'
    ENTRANCE_EXAM    = 'ENTRANCE_EXAM'
    OTHER            = 'OTHER'

    FEE_CATEGORIES = [
        (TUITION,          'Tuition / رسوم دراسية'),
        (ADMISSION,        'Admission Fee / رسوم القبول'),
        (REGISTRATION,     'Registration Fee / رسوم التسجيل'),
        (EXAMINATION,      'Examination Fee / رسوم الامتحان'),
        (TRANSPORT,        'Transport / مواصلات'),
        (UNIFORM,          'Uniform / زي مدرسي'),
        (BOOKS,            'Books & Supplies / كتب ومستلزمات'),
        (EXTRACURRICULAR,  'Extracurricular / أنشطة'),
        (LIBRARY,          'Library Fee / رسوم المكتبة'),
        (LABORATORY,       'Laboratory Fee / رسوم المختبر'),
        (SPORTS,           'Sports Fee / رسوم الرياضة'),
        (ANNUAL_FUNCTION,  'Annual Function Fee / رسوم الحفل السنوي'),
        (DEVELOPMENT,      'Development Fee / رسوم التطوير'),
        (SMART_CLASS,      'Smart Class / IT Fee / رسوم الفصل الذكي'),
        (ID_CARD,          'ID Card Fee / رسوم البطاقة'),
        (SECURITY_DEPOSIT, 'Security Deposit (Refundable) / تأمين'),
        (HOSTEL,           'Hostel Fee / رسوم السكن'),
        (MESS,             'Mess / Food Fee / رسوم الطعام'),
        (LATE_FEE,         'Late Fee / Fine / غرامة تأخير'),
        (RESERVATION,      'Reservation / حجز مقعد'),
        (ENTRANCE_EXAM,    'Entrance Exam / اختبار قبول'),
        (OTHER,            'Other / أخرى'),
    ]

    name           = models.CharField(max_length=100)
    category       = models.CharField(max_length=20, choices=FEE_CATEGORIES, default=OTHER)
    is_taxable     = models.BooleanField(default=False, help_text="Subject to VAT (ZATCA)")
    is_mandatory   = models.BooleanField(
        default=False,
        help_text="Auto-selected in every fee structure (cannot be unchecked)"
    )
    description    = models.TextField(blank=True)
    default_amount = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        help_text="Default price pre-filled when adding this fee to a structure (not used for Tuition)."
    )
    fixed_down_payment = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
        verbose_name='Fixed Down Payment (SAR)',
        help_text="If set, this amount is always required as the minimum down payment for this fee type."
    )

    VAT_RATE = Decimal('0.15')  # Saudi ZATCA standard rate for non-Saudi students

    def vat_rate_for(self, is_saudi: bool) -> 'Decimal':
        """
        Saudi students: 0% VAT on ALL fees (MoE exemption).
        Non-Saudi (expat) students: 15% VAT on taxable fees only.
        """
        if not self.is_taxable or is_saudi:
            return Decimal('0')
        return self.VAT_RATE

    class Meta:
        ordering = ['category', 'name']

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


# ════════════════════════════════════════════════════════════════
#  FEE STRUCTURE  (per grade / division / year)
# ════════════════════════════════════════════════════════════════

class FeeStructure(models.Model):
    """Container: one fee schedule per grade in an academic year."""
    TYPE_REGULAR = 'regular'
    TYPE_NEW     = 'new'
    TYPE_OTHER   = 'other'
    STRUCTURE_TYPE_CHOICES = [
        (TYPE_REGULAR, 'Regular'),
        (TYPE_NEW,     'New'),
        (TYPE_OTHER,   'Other'),
    ]

    name           = models.CharField(max_length=200, blank=True,
                                      help_text='Optional label, e.g. "Grade 1 American 2026-27"')
    structure_type = models.CharField(
        max_length=20, choices=STRUCTURE_TYPE_CHOICES, default=TYPE_REGULAR,
        verbose_name='Structure Type',
        help_text='"Regular" for returning students, "New" for new admissions')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT,
                                      related_name='fee_structures',
                                      verbose_name='Academic Year')
    grade         = models.ForeignKey(Grade, on_delete=models.PROTECT,
                                      related_name='fee_structures',
                                      verbose_name='Grade')
    frequency     = models.CharField(max_length=20, choices=[
        ('ONCE',    'One-time'),
        ('MONTHLY', 'Monthly'),
        ('TERM',    'Per Term'),
        ('ANNUAL',  'Annual'),
    ], default='ANNUAL')
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['academic_year', 'grade', 'structure_type']
        ordering = ['academic_year', 'grade__division__name', 'grade__order', 'grade__name', 'structure_type']

    def __str__(self):
        label = f"{self.grade} — {self.name}" if self.name else f"{self.grade} — Fee Structure"
        return f"{label} ({self.academic_year})"


class FeeStructureItem(models.Model):
    """One fee-type line within a FeeStructure container."""
    structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE,
                                  related_name='items')
    fee_type  = models.ForeignKey(FeeType, on_delete=models.PROTECT,
                                  related_name='structure_items')
    amount    = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ['structure', 'fee_type']
        ordering = ['fee_type__category', 'fee_type__name']

    def __str__(self):
        return f"{self.fee_type.name} — SAR {self.amount}"

    @property
    def expat_vat(self):
        if self.fee_type.is_taxable:
            return (self.amount * FeeType.VAT_RATE).quantize(Decimal('0.01'))
        return Decimal('0.00')

    @property
    def expat_total(self):
        return (self.amount + self.expat_vat).quantize(Decimal('0.01'))




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

    student       = models.ForeignKey(Student,           on_delete=models.CASCADE,
                                      related_name='fees')
    fee_structure = models.ForeignKey('FeeStructureItem', on_delete=models.PROTECT,
                                      related_name='student_fees')
    amount        = models.DecimalField(max_digits=10, decimal_places=2,
                                        help_text='Base amount (set at assignment time)')
    discount      = models.DecimalField(max_digits=10, decimal_places=2, default=0,
                                        help_text='Discount in SAR')
    discount_note = models.CharField(max_length=200, blank=True)
    net_amount    = models.DecimalField(max_digits=10, decimal_places=2,
                                        help_text='amount − discount + tax')
    due_date      = models.DateField()
    status        = models.CharField(max_length=10, choices=STATUS_CHOICES, default=UNPAID)
    created_at    = models.DateTimeField(auto_now_add=True)
    assigned_by   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                      null=True, blank=True, related_name='fees_assigned')

    class Meta:
        unique_together = ['student', 'fee_structure']
        ordering = ['due_date', 'student__full_name']

    def __str__(self):
        return f"{self.student} — {self.fee_structure.fee_type.name} — {self.status}"

    def save(self, *args, **kwargs):
        # Net = amount – discount + VAT on (amount – discount)
        base = self.amount - self.discount
        if base < 0:
            base = Decimal('0.00')
        rate = self.fee_structure.fee_type.vat_rate_for(self.student.is_saudi)
        self.net_amount = (base * (1 + rate)).quantize(Decimal('0.01'))
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
    CREDIT_CARD   = 'CREDIT_CARD'
    BANK          = 'BANK'
    INSTALLMENT   = 'INSTALLMENT'

    PAYMENT_METHODS = [
        (CREDIT_CARD,  'Credit Card / بطاقة ائتمانية'),
        (BANK,         'Bank Transfer / تحويل بنكي'),
        (INSTALLMENT,  'Installment / تقسيط'),
    ]

    student_fee    = models.ForeignKey(StudentFee, on_delete=models.CASCADE,
                                       related_name='payments')
    paid_amount    = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date   = models.DateField(default=timezone.localdate)
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHODS, default=CREDIT_CARD)
    receipt_number = models.CharField(max_length=30, unique=True,
                                      default=_receipt_number, editable=False)
    transaction_ref = models.CharField(max_length=100, blank=True,
                                       help_text="Bank ref / cheque no.")
    bank_verified    = models.BooleanField(default=False,
                                           help_text="Confirmed against bank statement")
    bank_verified_at = models.DateField(null=True, blank=True)
    notes          = models.TextField(blank=True)
    collected_by   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                       null=True, blank=True, related_name='payments_collected')

    class Meta:
        ordering = ['-payment_date', '-id']
        indexes = [
            models.Index(fields=['payment_date'], name='payment_date_idx'),
            models.Index(fields=['student_fee', 'payment_date'], name='payment_fee_date_idx'),
        ]

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

    CREDIT_NOTE = 'CREDIT_NOTE'

    STATUS_CHOICES = [
        (DRAFT,       'Draft'),
        (ISSUED,      'Issued'),
        (VOIDED,      'Voided'),
        (CREDIT_NOTE, 'Credit Note / إشعار دائن'),
    ]

    INVOICE_TYPE_STANDARD    = 'STANDARD'
    INVOICE_TYPE_CREDIT_NOTE = 'CREDIT_NOTE'
    INVOICE_TYPES = [
        (INVOICE_TYPE_STANDARD,    'Tax Invoice / فاتورة ضريبية'),
        (INVOICE_TYPE_CREDIT_NOTE, 'Tax Credit Note / إشعار دائن ضريبي'),
    ]

    student        = models.ForeignKey(Student, on_delete=models.PROTECT,
                                       related_name='invoices')
    invoice_number = models.CharField(max_length=40, unique=True,
                                      default=_invoice_number, editable=False)
    date           = models.DateField(default=timezone.localdate)
    subtotal       = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax_amount     = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total          = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status         = models.CharField(max_length=15, choices=STATUS_CHOICES, default=DRAFT)
    invoice_type   = models.CharField(max_length=15, choices=INVOICE_TYPES,
                                      default=INVOICE_TYPE_STANDARD)
    notes          = models.TextField(blank=True)
    created_by     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                       null=True, blank=True, related_name='invoices_created')
    # Line items stored as JSON snapshot
    line_items_json = models.JSONField(default=list, blank=True)

    # Credit note linkage
    original_invoice   = models.ForeignKey(
        'self', null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='credit_notes',
        help_text='The original invoice this credit note refers to (if any).',
    )
    credit_note_reason = models.TextField(blank=True, help_text='Reason for issuing credit note.')

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
        return f"{self.staff.full_name or self.staff.username} — {self.month.strftime('%b %Y')} — SAR {self.net_salary}"

    def save(self, *args, **kwargs):
        allowances    = self.housing + self.transport + self.other_allowances
        self.net_salary = self.basic + allowances - self.deductions
        if self.net_salary < 0:
            self.net_salary = Decimal('0.00')
        super().save(*args, **kwargs)


# ════════════════════════════════════════════════════════════════
#  TUITION FEE CONFIG  (complete fee structure per division/grade/year)
# ════════════════════════════════════════════════════════════════

class TuitionFeeConfig(models.Model):
    REGULAR = 'REGULAR'
    SPECIAL = 'SPECIAL'
    STRUCTURE_TYPE_CHOICES = [
        (REGULAR, 'Regular'),
        (SPECIAL, 'Special / New Students'),
    ]

    PAYMENTS_2 = 2
    PAYMENTS_3 = 3
    NUM_PAYMENTS_CHOICES = [
        (PAYMENTS_2, '2 Installments'),
        (PAYMENTS_3, '3 Installments'),
    ]

    academic_year          = models.ForeignKey(
        AcademicYear, on_delete=models.PROTECT, related_name='tuition_configs')
    division               = models.ForeignKey(
        Division, on_delete=models.PROTECT, related_name='tuition_configs')
    grade                  = models.ForeignKey(
        Grade, on_delete=models.PROTECT, related_name='tuition_configs')
    structure_type         = models.CharField(
        max_length=10, choices=STRUCTURE_TYPE_CHOICES, default=REGULAR)
    num_payments           = models.PositiveSmallIntegerField(
        choices=NUM_PAYMENTS_CHOICES, default=PAYMENTS_2,
        verbose_name='Number of Installments')
    includes_books         = models.BooleanField(
        default=False, help_text='Tuition fee includes books')

    # ── One-time fees ─────────────────────────────────────────────
    entrance_exam_fee      = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0.00'),
        verbose_name='Entrance Exam Fee (SAR)')
    registration_fee       = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0.00'),
        verbose_name='Registration Fee (SAR)')
    reservation_fee        = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0.00'),
        help_text='Down payment / حجز مقعد',
        verbose_name='Reservation / Down Payment (SAR)')

    # ── Tuition ───────────────────────────────────────────────────
    gross_tuition_fee      = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name='Gross Tuition Fee (SAR)')

    # ── Group discount ────────────────────────────────────────────
    group_discount_enabled = models.BooleanField(default=False)
    group_discount_pct     = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal('0.00'),
        help_text='Discount percentage (e.g. 10 for 10%)',
        verbose_name='Group Discount (%)')

    # ── VAT ───────────────────────────────────────────────────────
    vat_pct                = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal('15.00'),
        help_text='VAT rate (%) applied to non-Saudi students',
        verbose_name='VAT Rate (%)')

    # ── Year range (multi-year applicability) ─────────────────────
    from_academic_year     = models.ForeignKey(
        AcademicYear, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='tuition_configs_from', verbose_name='Applicable From Year')
    to_academic_year       = models.ForeignKey(
        AcademicYear, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='tuition_configs_to', verbose_name='Applicable To Year')

    notes      = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['academic_year', 'division', 'grade', 'structure_type']
        ordering = ['division__name', 'grade__order', 'grade__name', 'structure_type']
        verbose_name = 'Tuition Fee Configuration'
        verbose_name_plural = 'Tuition Fee Configurations'

    def __str__(self):
        return (f"{self.division} — {self.grade} — "
                f"{self.get_structure_type_display()} ({self.academic_year})")

    # ── Computed fee components ───────────────────────────────────

    @property
    def group_discount_amount(self) -> Decimal:
        """Group discount in SAR."""
        if not self.group_discount_enabled or self.group_discount_pct <= 0:
            return Decimal('0.00')
        return (self.gross_tuition_fee * self.group_discount_pct / 100).quantize(Decimal('0.01'))

    @property
    def net_tuition_fee(self) -> Decimal:
        """Net tuition after group discount (Saudi students pay this amount)."""
        return (self.gross_tuition_fee - self.group_discount_amount).quantize(Decimal('0.01'))

    @property
    def vat_amount_non_saudi(self) -> Decimal:
        """VAT amount charged to non-Saudi students on net tuition."""
        return (self.net_tuition_fee * self.vat_pct / 100).quantize(Decimal('0.01'))

    @property
    def final_net_non_saudi(self) -> Decimal:
        """Total tuition for non-Saudi students (net tuition + VAT)."""
        return (self.net_tuition_fee + self.vat_amount_non_saudi).quantize(Decimal('0.01'))

    @property
    def total_one_time_fees(self) -> Decimal:
        """Sum of entrance exam + registration + reservation fees."""
        return (
            self.entrance_exam_fee + self.registration_fee + self.reservation_fee
        ).quantize(Decimal('0.01'))

    @property
    def installments_total(self) -> Decimal:
        """Sum of all non-reservation installments."""
        total = Decimal('0.00')
        for inst in self.installments.all():
            if inst.installment_type != TuitionInstallment.RESERVATION:
                total += inst.amount
        return total.quantize(Decimal('0.01'))

    def validate_installments(self) -> list:
        """Return list of validation error strings. Empty list = valid."""
        errors = []
        insts = list(self.installments.all())
        if not insts:
            return errors

        # Reservation installment must match reservation_fee
        res_insts = [i for i in insts if i.installment_type == TuitionInstallment.RESERVATION]
        if res_insts:
            res_total = sum(i.amount for i in res_insts)
            if abs(res_total - self.reservation_fee) > Decimal('0.01'):
                errors.append(
                    f"Reservation installment ({res_total:,.2f}) ≠ "
                    f"reservation fee ({self.reservation_fee:,.2f})."
                )

        # Non-reservation installments must sum to net_tuition_fee
        non_res = [i for i in insts if i.installment_type != TuitionInstallment.RESERVATION]
        if non_res:
            non_res_total = sum(i.amount for i in non_res)
            if abs(non_res_total - self.net_tuition_fee) > Decimal('0.01'):
                errors.append(
                    f"Installments (excl. reservation) total SAR {non_res_total:,.2f} ≠ "
                    f"net tuition SAR {self.net_tuition_fee:,.2f}."
                )

        # Installment count must match num_payments
        if len(non_res) != self.num_payments:
            errors.append(
                f"Expected {self.num_payments} installment(s), found {len(non_res)}."
            )
        return errors


# ════════════════════════════════════════════════════════════════
#  PAYMENT PLAN  (per-student installment schedule for a StudentFee)
# ════════════════════════════════════════════════════════════════

class PaymentPlan(models.Model):
    """Installment schedule attached to one StudentFee."""
    student_fee = models.OneToOneField(
        StudentFee, on_delete=models.CASCADE, related_name='payment_plan')
    notes       = models.TextField(blank=True)
    created_by  = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='payment_plans_created')
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"Plan — {self.student_fee.student} — "
                f"{self.student_fee.fee_structure.fee_type.name}")


class PaymentPlanInstallment(models.Model):
    UNPAID  = 'UNPAID'
    PARTIAL = 'PARTIAL'
    PAID    = 'PAID'
    OVERDUE = 'OVERDUE'

    STATUS_CHOICES = [
        (UNPAID,  'Unpaid'),
        (PARTIAL, 'Partial'),
        (PAID,    'Paid'),
        (OVERDUE, 'Overdue'),
    ]

    plan           = models.ForeignKey(
        PaymentPlan, on_delete=models.CASCADE, related_name='installments')
    installment_no = models.PositiveSmallIntegerField()
    amount         = models.DecimalField(max_digits=10, decimal_places=2)
    due_date       = models.DateField()
    paid_amount    = models.DecimalField(
        max_digits=10, decimal_places=2, default=Decimal('0.00'))
    status         = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default=UNPAID)

    class Meta:
        ordering = ['installment_no']
        unique_together = ['plan', 'installment_no']

    def __str__(self):
        return (f"Installment {self.installment_no} — "
                f"{self.plan.student_fee.student} — SAR {self.amount:,.2f}")

    @property
    def balance(self):
        return (self.amount - self.paid_amount).quantize(Decimal('0.01'))

    def refresh_status(self):
        if self.paid_amount <= 0:
            self.status = (
                self.OVERDUE if self.due_date < timezone.localdate() else self.UNPAID
            )
        elif self.paid_amount >= self.amount:
            self.status = self.PAID
        else:
            self.status = self.PARTIAL
        self.save(update_fields=['status'])


class TuitionInstallment(models.Model):
    RESERVATION = 'RESERVATION'
    FIRST       = 'FIRST'
    SECOND      = 'SECOND'
    THIRD       = 'THIRD'

    INSTALLMENT_TYPES = [
        (RESERVATION, 'Reservation / Down Payment'),
        (FIRST,       '1st Installment'),
        (SECOND,      '2nd Installment'),
        (THIRD,       '3rd Installment'),
    ]

    # For deterministic ordering without DB-level sort
    INSTALLMENT_ORDER = {RESERVATION: 0, FIRST: 1, SECOND: 2, THIRD: 3}

    config           = models.ForeignKey(
        TuitionFeeConfig, on_delete=models.CASCADE, related_name='installments')
    installment_type = models.CharField(max_length=15, choices=INSTALLMENT_TYPES)
    amount           = models.DecimalField(max_digits=10, decimal_places=2)
    due_date         = models.DateField(null=True, blank=True)
    notes            = models.CharField(max_length=200, blank=True)

    class Meta:
        unique_together = ['config', 'installment_type']
        ordering = ['config', 'installment_type']
        verbose_name = 'Tuition Installment'
        verbose_name_plural = 'Tuition Installments'

    def __str__(self):
        return (f"{self.config} — {self.get_installment_type_display()} "
                f"— SAR {self.amount:,.2f}")


# ════════════════════════════════════════════════════════════════
#  EXTERNAL CANDIDATE  (non-enrolled students taking board exams)
# ════════════════════════════════════════════════════════════════

def _candidate_id():
    ts  = timezone.now().strftime('%Y%m%d')
    uid = str(uuid.uuid4().int)[:5]
    return f"EXT-{ts}-{uid}"


class ExternalCandidate(models.Model):
    """Lightweight record for pending admissions and external exam candidates."""

    STATUS_PENDING = 'PENDING'
    STATUS_APPROVED = 'APPROVED'
    STATUS_REJECTED = 'REJECTED'
    STATUS_CHOICES = [
        (STATUS_PENDING, 'Pending / قيد الانتظار'),
        (STATUS_APPROVED, 'Approved (Enrolled) / معتمد'),
        (STATUS_REJECTED, 'Rejected / مرفوض'),
    ]

    candidate_id    = models.CharField(
        max_length=30, unique=True, default=_candidate_id, editable=False,
        verbose_name='Candidate ID')
    full_name       = models.CharField(max_length=200, verbose_name='Full Name (English)')
    arabic_name     = models.CharField(max_length=200, blank=True, verbose_name='الاسم (عربي)')
    phone           = models.CharField(max_length=20, blank=True, verbose_name='Phone / رقم الجوال')
    nationality     = models.CharField(max_length=100, blank=True, verbose_name='Nationality / الجنسية')
    id_number       = models.CharField(
        max_length=50, blank=True, verbose_name='ID / Iqama / Passport',
        help_text='National ID, Iqama, or Passport number')
    grade_applying  = models.ForeignKey(
        Grade, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='external_candidates', verbose_name='Grade Applying For / الصف')
    division        = models.ForeignKey(
        'core.Division', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='external_candidates',
        verbose_name='Division / القسم',
        help_text='School division (American, British, French, Home Study)')
    board           = models.ForeignKey(
        'core.Board', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='external_candidates',
        verbose_name='Board / Entrance Exam',
        help_text='Which board entrance exam is the candidate taking?')
    notes           = models.TextField(blank=True)
    status          = models.CharField(max_length=15, choices=STATUS_CHOICES, default=STATUS_PENDING, verbose_name='Admission Status')
    enrolled_student = models.OneToOneField(
        Student, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='admission_application',
        help_text='Linked student record if approved and enrolled'
    )
    is_saudi        = models.BooleanField(
        null=True, blank=True,
        verbose_name='Saudi National / مواطن سعودي',
        help_text='True = Saudi (0% VAT), False/None = Non-Saudi (15% VAT on taxable fees)')
    is_active       = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)
    created_by      = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='external_candidates_created')

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'External Candidate / مرشح خارجي'
        verbose_name_plural = 'External Candidates / مرشحون خارجيون'

    def __str__(self):
        return f"[{self.candidate_id}] {self.full_name}"


def _ext_receipt_number():
    return "EXT-" + str(uuid.uuid4().int)[:8].upper()


class ExternalCandidatePayment(models.Model):
    """Payment record for an external candidate's exam or other fees."""

    CREDIT_CARD = 'CREDIT_CARD'
    BANK        = 'BANK'
    CASH        = 'CASH'

    PAYMENT_METHODS = [
        (CASH,        'Cash / نقدي'),
        (CREDIT_CARD, 'Credit Card / بطاقة ائتمانية'),
        (BANK,        'Bank Transfer / تحويل بنكي'),
    ]

    candidate       = models.ForeignKey(
        ExternalCandidate, on_delete=models.CASCADE, related_name='payments')
    fee_description = models.CharField(max_length=200, verbose_name='Fee Description')
    amount          = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Amount (SAR)')
    vat_rate        = models.DecimalField(
        max_digits=5, decimal_places=2, default=Decimal('0.00'),
        verbose_name='VAT Rate (%)')
    vat_amount      = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total           = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    payment_method  = models.CharField(max_length=15, choices=PAYMENT_METHODS, default=CASH)
    payment_date    = models.DateField(default=timezone.localdate)
    receipt_number  = models.CharField(
        max_length=30, unique=True, default=_ext_receipt_number, editable=False)
    transaction_ref = models.CharField(max_length=100, blank=True, help_text='Bank ref / cheque no.')
    notes           = models.TextField(blank=True)
    invoice         = models.ForeignKey(
        TaxInvoice, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='external_payments',
        help_text='ZATCA Tax Invoice generated for this payment')
    collected_by    = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='ext_payments_collected')
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-payment_date', '-id']
        verbose_name = 'External Candidate Payment'

    def __str__(self):
        return f"{self.receipt_number} — {self.candidate.full_name} — SAR {self.total}"

    def save(self, *args, **kwargs):
        self.vat_amount = (self.amount * self.vat_rate / 100).quantize(Decimal('0.01'))
        self.total = self.amount + self.vat_amount
        super().save(*args, **kwargs)
