from django import forms
from django.utils import timezone
from core.models import AcademicYear, Division, Grade, Section
from .models import (
    FeeType, FeeStructure, StudentFee, Payment, TaxInvoice, Salary,
    TuitionFeeConfig, TuitionInstallment,
)

_INPUT  = ('border border-slate-300 rounded-lg px-3 py-2 w-full text-sm '
           'focus:ring-2 focus:ring-primary/40 focus:border-primary focus:outline-none')
_SELECT = _INPUT
_SMALL  = ('border border-slate-300 rounded-lg px-3 py-2 w-full text-sm '
           'focus:ring-2 focus:ring-primary/40 focus:outline-none bg-white')


class FeeTypeForm(forms.ModelForm):
    class Meta:
        model  = FeeType
        fields = ['name', 'category', 'is_taxable', 'description']
        widgets = {
            'name':        forms.TextInput(attrs={'class': _INPUT}),
            'category':    forms.Select(attrs={'class': _SELECT}),
            'description': forms.Textarea(attrs={'class': _INPUT, 'rows': 2}),
        }


class FeeStructureForm(forms.ModelForm):
    class Meta:
        model  = FeeStructure
        fields = ['academic_year', 'grade', 'division', 'fee_type', 'amount', 'due_date', 'frequency']
        widgets = {
            'academic_year': forms.Select(attrs={'class': _SELECT}),
            'grade':         forms.Select(attrs={'class': _SELECT}),
            'division':      forms.Select(attrs={'class': _SELECT}),
            'fee_type':      forms.Select(attrs={'class': _SELECT}),
            'amount':        forms.NumberInput(attrs={'class': _INPUT, 'step': '0.01', 'min': '0'}),
            'due_date':      forms.DateInput(attrs={'class': _INPUT, 'type': 'date'}),
            'frequency':     forms.Select(attrs={'class': _SELECT}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['academic_year'].queryset = AcademicYear.objects.all()


class BulkAssignFeeForm(forms.Form):
    """Assign a FeeStructure to all students in a grade (or specific section)."""
    fee_structure  = forms.ModelChoiceField(
        queryset=FeeStructure.objects.select_related('fee_type', 'grade', 'academic_year'),
        widget=forms.Select(attrs={'class': _SELECT}),
        label='Fee Structure',
    )
    section        = forms.ModelChoiceField(
        queryset=Section.objects.select_related('grade'),
        required=False,
        widget=forms.Select(attrs={'class': _SELECT}),
        label='Section (leave blank = entire grade)',
        empty_label='All Sections',
    )
    discount       = forms.DecimalField(
        required=False, initial=0, min_value=0,
        widget=forms.NumberInput(attrs={'class': _INPUT, 'step': '0.01'}),
        label='Blanket Discount (SAR)',
    )
    discount_note  = forms.CharField(
        required=False, max_length=200,
        widget=forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'e.g. Sibling discount'}),
    )

    def clean_discount(self):
        return self.cleaned_data.get('discount') or 0


class StudentFeeEditForm(forms.ModelForm):
    """Edit discount on an individual StudentFee."""
    class Meta:
        model  = StudentFee
        fields = ['discount', 'discount_note', 'due_date', 'status']
        widgets = {
            'discount':      forms.NumberInput(attrs={'class': _INPUT, 'step': '0.01', 'min': '0'}),
            'discount_note': forms.TextInput(attrs={'class': _INPUT}),
            'due_date':      forms.DateInput(attrs={'class': _INPUT, 'type': 'date'}),
            'status':        forms.Select(attrs={'class': _SELECT}),
        }


class PaymentForm(forms.ModelForm):
    # Optional discount to apply on the spot (updates StudentFee.discount)
    apply_discount = forms.DecimalField(
        required=False, min_value=0, decimal_places=2,
        widget=forms.NumberInput(attrs={
            'class': _INPUT, 'step': '0.01', 'min': '0',
            'placeholder': '0.00', 'id': 'id_apply_discount',
        }),
        label='Discount to Apply (SAR)',
    )
    discount_note = forms.CharField(
        required=False, max_length=200,
        widget=forms.TextInput(attrs={
            'class': _INPUT, 'placeholder': 'e.g. Sibling discount, scholarship…',
        }),
        label='Discount Reason',
    )

    class Meta:
        model  = Payment
        fields = ['paid_amount', 'payment_date', 'payment_method', 'transaction_ref', 'notes']
        widgets = {
            'paid_amount':     forms.NumberInput(attrs={
                'class': _INPUT, 'step': '0.01', 'min': '0.01',
                'id': 'id_paid_amount', 'placeholder': 'Enter amount collected',
            }),
            'payment_date':    forms.DateInput(attrs={'class': _INPUT, 'type': 'date'}),
            'payment_method':  forms.Select(attrs={'class': _SELECT}),
            'transaction_ref': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Bank ref / cheque no.'}),
            'notes':           forms.Textarea(attrs={'class': _INPUT, 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_date'].initial = timezone.localdate()
        # paid_amount is intentionally NOT pre-filled — accountant enters what was collected


class FeeReportFilterForm(forms.Form):
    academic_year = forms.ModelChoiceField(
        queryset=AcademicYear.objects.all(),
        required=False,
        empty_label='All Years',
        widget=forms.Select(attrs={'class': _SMALL}),
    )
    division = forms.ModelChoiceField(
        queryset=Division.objects.all(),
        required=False,
        empty_label='All Divisions',
        widget=forms.Select(attrs={'class': _SMALL}),
    )
    grade = forms.ModelChoiceField(
        queryset=Grade.objects.select_related('division').all(),
        required=False,
        empty_label='All Grades',
        widget=forms.Select(attrs={'class': _SMALL}),
    )
    section = forms.ModelChoiceField(
        queryset=Section.objects.select_related('grade').all(),
        required=False,
        empty_label='All Sections',
        widget=forms.Select(attrs={'class': _SMALL}),
    )
    status = forms.ChoiceField(
        choices=[('', 'All Statuses')] + StudentFee.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': _SMALL}),
    )
    fee_type = forms.ModelChoiceField(
        queryset=FeeType.objects.all(),
        required=False,
        empty_label='All Fee Types',
        widget=forms.Select(attrs={'class': _SMALL}),
    )
    as_of_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': _SMALL, 'type': 'date'}),
        label='As of Date',
        help_text='Show fees due on or before this date',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            current = AcademicYear.objects.filter(is_current=True).first()
            if current:
                self.fields['academic_year'].initial = current.pk
        except Exception:
            pass


class SalaryForm(forms.ModelForm):
    class Meta:
        model  = Salary
        fields = ['staff', 'month', 'basic', 'housing', 'transport',
                  'other_allowances', 'deductions', 'is_paid', 'paid_date', 'bank_ref', 'notes']
        widgets = {
            'staff':            forms.Select(attrs={'class': _SELECT}),
            'month':            forms.DateInput(attrs={'class': _INPUT, 'type': 'date',
                                                       'placeholder': 'YYYY-MM-01'}),
            'basic':            forms.NumberInput(attrs={'class': _INPUT, 'step': '0.01'}),
            'housing':          forms.NumberInput(attrs={'class': _INPUT, 'step': '0.01'}),
            'transport':        forms.NumberInput(attrs={'class': _INPUT, 'step': '0.01'}),
            'other_allowances': forms.NumberInput(attrs={'class': _INPUT, 'step': '0.01'}),
            'deductions':       forms.NumberInput(attrs={'class': _INPUT, 'step': '0.01'}),
            'paid_date':        forms.DateInput(attrs={'class': _INPUT, 'type': 'date'}),
            'bank_ref':         forms.TextInput(attrs={'class': _INPUT}),
            'notes':            forms.Textarea(attrs={'class': _INPUT, 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from accounts.models import CustomUser
        self.fields['staff'].queryset = CustomUser.objects.filter(
            role__in=['TEACHER', 'ACCOUNTANT', 'STAFF', 'ADMIN', 'SUPER_ADMIN'],
            is_active=True,
        ).order_by('full_name')


class SalaryMonthFilterForm(forms.Form):
    month = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': _INPUT, 'type': 'month'}),
        label='Month',
    )


class ManualInvoiceLineForm(forms.Form):
    """One line item on a manually-entered tax invoice."""
    description = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'e.g. Reservation Seat Fee'}),
    )
    amount = forms.DecimalField(
        min_value=0, decimal_places=2,
        widget=forms.NumberInput(attrs={'class': _INPUT, 'step': '0.01', 'min': '0'}),
    )
    is_taxable = forms.BooleanField(required=False, label='Subject to 15% VAT')
    is_credit  = forms.BooleanField(required=False, label='Credit / Deduction (negative line)')


class ManualInvoiceHeaderForm(forms.Form):
    """Header fields for a manually-entered tax invoice."""
    INVOICE_TYPES = [
        ('STANDARD',    'Tax Invoice (Standard)'),
        ('CREDIT_NOTE', 'Tax Credit Note (Discount / Refund)'),
    ]
    invoice_type = forms.ChoiceField(
        choices=INVOICE_TYPES,
        widget=forms.Select(attrs={'class': _SELECT}),
        label='Invoice Type',
    )
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': _INPUT, 'type': 'date'}),
        initial=__import__('datetime').date.today,
    )
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': _INPUT, 'rows': 2,
                                     'placeholder': 'Optional notes…'}),
    )


class DefaultersFilterForm(forms.Form):
    """Filter form for the defaulters list."""
    as_of_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': _SMALL, 'type': 'date'}),
        label='As of Date',
    )
    grade = forms.ModelChoiceField(
        queryset=__import__('core.models', fromlist=['Grade']).Grade.objects.all(),
        required=False,
        empty_label='All Grades',
        widget=forms.Select(attrs={'class': _SMALL}),
    )
    division = forms.ModelChoiceField(
        queryset=__import__('core.models', fromlist=['Division']).Division.objects.all(),
        required=False,
        empty_label='All Divisions',
        widget=forms.Select(attrs={'class': _SMALL}),
    )


# ════════════════════════════════════════════════════════════════
#  TUITION FEE CONFIG FORMS
# ════════════════════════════════════════════════════════════════

class TuitionFeeConfigForm(forms.ModelForm):
    class Meta:
        model  = TuitionFeeConfig
        fields = [
            'academic_year', 'division', 'grade', 'structure_type',
            'num_payments', 'includes_books',
            'entrance_exam_fee', 'registration_fee', 'reservation_fee',
            'gross_tuition_fee',
            'group_discount_enabled', 'group_discount_pct',
            'vat_pct',
            'from_academic_year', 'to_academic_year',
            'notes',
        ]
        widgets = {
            'academic_year':          forms.Select(attrs={'class': _SELECT}),
            'division':               forms.Select(attrs={'class': _SELECT}),
            'grade':                  forms.Select(attrs={'class': _SELECT}),
            'structure_type':         forms.Select(attrs={'class': _SELECT}),
            'num_payments':           forms.Select(attrs={'class': _SELECT}),
            'includes_books':         forms.CheckboxInput(),
            'entrance_exam_fee':      forms.NumberInput(attrs={
                'class': _INPUT, 'step': '0.01', 'min': '0'}),
            'registration_fee':       forms.NumberInput(attrs={
                'class': _INPUT, 'step': '0.01', 'min': '0'}),
            'reservation_fee':        forms.NumberInput(attrs={
                'class': _INPUT, 'step': '0.01', 'min': '0'}),
            'gross_tuition_fee':      forms.NumberInput(attrs={
                'class': _INPUT, 'step': '0.01', 'min': '0'}),
            'group_discount_enabled': forms.CheckboxInput(),
            'group_discount_pct':     forms.NumberInput(attrs={
                'class': _INPUT, 'step': '0.01', 'min': '0', 'max': '100'}),
            'vat_pct':                forms.NumberInput(attrs={
                'class': _INPUT, 'step': '0.01', 'min': '0', 'max': '100'}),
            'from_academic_year':     forms.Select(attrs={'class': _SELECT}),
            'to_academic_year':       forms.Select(attrs={'class': _SELECT}),
            'notes':                  forms.Textarea(attrs={'class': _INPUT, 'rows': 2}),
        }

    def clean(self):
        cleaned = super().clean()
        disc_enabled = cleaned.get('group_discount_enabled')
        disc_pct     = cleaned.get('group_discount_pct') or 0
        if disc_enabled and disc_pct <= 0:
            self.add_error('group_discount_pct',
                           'Enter a discount percentage when group discount is enabled.')
        if not disc_enabled:
            cleaned['group_discount_pct'] = 0
        gross = cleaned.get('gross_tuition_fee')
        res   = cleaned.get('reservation_fee', 0) or 0
        if gross and res > gross:
            self.add_error('reservation_fee',
                           'Reservation fee cannot exceed gross tuition fee.')
        return cleaned


class TuitionInstallmentForm(forms.ModelForm):
    class Meta:
        model  = TuitionInstallment
        fields = ['installment_type', 'amount', 'due_date', 'notes']
        widgets = {
            'installment_type': forms.Select(attrs={'class': _SELECT}),
            'amount':           forms.NumberInput(attrs={
                'class': _INPUT, 'step': '0.01', 'min': '0'}),
            'due_date':         forms.DateInput(attrs={'class': _INPUT, 'type': 'date'}),
            'notes':            forms.TextInput(attrs={'class': _INPUT}),
        }


TuitionInstallmentFormSet = forms.inlineformset_factory(
    TuitionFeeConfig,
    TuitionInstallment,
    form=TuitionInstallmentForm,
    extra=4,
    can_delete=True,
    max_num=4,
)


class TuitionConfigFilterForm(forms.Form):
    """Filter form for tuition config list."""
    academic_year = forms.ModelChoiceField(
        queryset=AcademicYear.objects.all(),
        required=False,
        empty_label='All Years',
        widget=forms.Select(attrs={'class': _SMALL}),
    )
    division = forms.ModelChoiceField(
        queryset=Division.objects.filter(is_active=True),
        required=False,
        empty_label='All Divisions',
        widget=forms.Select(attrs={'class': _SMALL}),
    )
    structure_type = forms.ChoiceField(
        choices=[('', 'All Types')] + TuitionFeeConfig.STRUCTURE_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': _SMALL}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            current = AcademicYear.objects.filter(is_current=True).first()
            if current:
                self.fields['academic_year'].initial = current.pk
        except Exception:
            pass
