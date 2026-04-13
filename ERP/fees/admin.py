from django.contrib import admin
from .models import FeeType, FeeStructure, StudentFee, Payment, TaxInvoice, Salary


class PaymentInline(admin.TabularInline):
    model  = Payment
    extra  = 0
    fields = ('paid_amount', 'payment_date', 'payment_method', 'receipt_number', 'collected_by')
    readonly_fields = ('receipt_number',)


@admin.register(FeeType)
class FeeTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'is_taxable')
    list_filter  = ('category', 'is_taxable')


@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display  = ('fee_type', 'grade', 'division', 'academic_year', 'amount', 'due_date')
    list_filter   = ('academic_year', 'grade', 'division')
    search_fields = ('fee_type__name',)


@admin.register(StudentFee)
class StudentFeeAdmin(admin.ModelAdmin):
    list_display  = ('student', 'fee_structure', 'net_amount', 'status', 'due_date')
    list_filter   = ('status', 'fee_structure__academic_year')
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
