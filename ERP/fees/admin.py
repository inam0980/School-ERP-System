from django.contrib import admin
from .models import (
    FeeType, FeeStructure, FeeStructureItem, StudentFee, Payment, TaxInvoice, Salary,
    TuitionFeeConfig, TuitionInstallment,
    ExternalCandidate, ExternalCandidatePayment,
)


class PaymentInline(admin.TabularInline):
    model  = Payment
    extra  = 0
    fields = ('paid_amount', 'payment_date', 'payment_method', 'receipt_number', 'collected_by')
    readonly_fields = ('receipt_number',)


class FeeStructureItemInline(admin.TabularInline):
    model  = FeeStructureItem
    extra  = 1
    fields = ('fee_type', 'amount')


@admin.register(FeeType)
class FeeTypeAdmin(admin.ModelAdmin):
    list_display  = ('name', 'category', 'is_taxable', 'is_mandatory', 'default_amount', 'fixed_down_payment')
    list_filter   = ('category', 'is_taxable', 'is_mandatory')
    list_editable = ('is_mandatory', 'fixed_down_payment')


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display  = ('__str__', 'grade', 'academic_year', 'frequency')
    list_filter   = ('academic_year', 'grade__division')
    search_fields = ('name', 'grade__name', 'grade__division__name')
    inlines       = [FeeStructureItemInline]


@admin.register(FeeStructureItem)
class FeeStructureItemAdmin(admin.ModelAdmin):
    list_display  = ('fee_type', 'structure', 'amount')
    list_filter   = ('structure__academic_year', 'structure__grade__division', 'fee_type__category')
    search_fields = ('fee_type__name',)


@admin.register(StudentFee)
class StudentFeeAdmin(admin.ModelAdmin):
    list_display  = ('student', 'fee_structure', 'net_amount', 'status', 'due_date')
    list_filter   = ('status', 'fee_structure__structure__academic_year')
    search_fields = ('student__full_name', 'student__student_id')
    inlines       = [PaymentInline]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display  = ('receipt_number', 'student_fee', 'paid_amount', 'payment_date', 'payment_method')
    list_filter   = ('payment_method', 'payment_date')
    search_fields = ('receipt_number', 'student_fee__student__full_name')
    readonly_fields = ('receipt_number',)


@admin.register(TaxInvoice)
class TaxInvoiceAdmin(admin.ModelAdmin):
    list_display  = ('invoice_number', 'student', 'total', 'status', 'date')
    list_filter   = ('status',)
    search_fields = ('invoice_number', 'student__full_name')
    readonly_fields = ('invoice_number',)


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display  = ('staff', 'month', 'basic', 'net_salary', 'is_paid')
    list_filter   = ('is_paid', 'month')
    search_fields = ('staff__first_name', 'staff__last_name', 'staff__username')
    readonly_fields = ('net_salary',)


# ════════════════════════════════════════════════════════════════
#  TUITION FEE CONFIG
# ════════════════════════════════════════════════════════════════

class TuitionInstallmentInline(admin.TabularInline):
    model  = TuitionInstallment
    extra  = 0
    fields = ('installment_type', 'amount', 'due_date', 'notes')


@admin.register(TuitionFeeConfig)
class TuitionFeeConfigAdmin(admin.ModelAdmin):
    list_display   = (
        'academic_year', 'division', 'grade', 'structure_type',
        'gross_tuition_fee', '_net_tuition', '_vat_non_saudi', '_final_non_saudi',
        'num_payments', 'includes_books',
    )
    list_filter    = ('academic_year', 'division', 'structure_type', 'includes_books')
    search_fields  = ('grade__name', 'division__name')
    readonly_fields = (
        '_group_discount_amount', '_net_tuition', '_vat_non_saudi', '_final_non_saudi',
    )
    inlines        = [TuitionInstallmentInline]
    fieldsets      = [
        ('Identification', {
            'fields': ('academic_year', 'division', 'grade',
                       'structure_type', 'num_payments', 'includes_books',
                       'from_academic_year', 'to_academic_year'),
        }),
        ('One-time Fees', {
            'fields': ('entrance_exam_fee', 'registration_fee', 'reservation_fee'),
        }),
        ('Tuition & Discount', {
            'fields': ('gross_tuition_fee', 'group_discount_enabled',
                       'group_discount_pct', '_group_discount_amount'),
        }),
        ('Computed (read-only)', {
            'fields': ('_net_tuition', 'vat_pct', '_vat_non_saudi', '_final_non_saudi'),
        }),
        ('Notes', {'fields': ('notes',)}),
    ]

    @admin.display(description='Group Discount (SAR)')
    def _group_discount_amount(self, obj):
        return f"SAR {obj.group_discount_amount:,.2f}"

    @admin.display(description='Net Tuition – Saudi')
    def _net_tuition(self, obj):
        return f"SAR {obj.net_tuition_fee:,.2f}"

    @admin.display(description='VAT – Non-Saudi')
    def _vat_non_saudi(self, obj):
        return f"SAR {obj.vat_amount_non_saudi:,.2f}"

    @admin.display(description='Final – Non-Saudi')
    def _final_non_saudi(self, obj):
        return f"SAR {obj.final_net_non_saudi:,.2f}"


@admin.register(TuitionInstallment)
class TuitionInstallmentAdmin(admin.ModelAdmin):
    list_display  = ('config', 'installment_type', 'amount', 'due_date')
    list_filter   = ('installment_type', 'config__academic_year', 'config__division')
    search_fields = ('config__grade__name',)


# ════════════════════════════════════════════════════════════════
#  EXTERNAL CANDIDATE
# ════════════════════════════════════════════════════════════════

class ExternalCandidatePaymentInline(admin.TabularInline):
    model  = ExternalCandidatePayment
    extra  = 0
    fields = ('fee_description', 'amount', 'vat_amount', 'total', 'payment_method',
              'payment_date', 'receipt_number')
    readonly_fields = ('receipt_number', 'vat_amount', 'total')


@admin.register(ExternalCandidate)
class ExternalCandidateAdmin(admin.ModelAdmin):
    list_display  = ('candidate_id', 'full_name', 'arabic_name', 'phone',
                     'board', 'grade_applying', 'is_active', 'created_at')
    list_filter   = ('is_active', 'board', 'grade_applying')
    search_fields = ('full_name', 'arabic_name', 'candidate_id', 'phone', 'id_number')
    readonly_fields = ('candidate_id',)
    inlines       = [ExternalCandidatePaymentInline]


@admin.register(ExternalCandidatePayment)
class ExternalCandidatePaymentAdmin(admin.ModelAdmin):
    list_display  = ('receipt_number', 'candidate', 'fee_description', 'total',
                     'payment_method', 'payment_date')
    list_filter   = ('payment_method', 'payment_date')
    search_fields = ('receipt_number', 'candidate__full_name', 'candidate__candidate_id')
    readonly_fields = ('receipt_number', 'vat_amount', 'total')

