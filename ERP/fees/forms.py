from django import forms
from django.utils import timezone
from core.models import AcademicYear, Division, Grade, Section
from .models import FeeType, FeeStructure, StudentFee, Payment, TaxInvoice, Salary

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
    class Meta:
        model  = Payment
        fields = ['paid_amount', 'payment_date', 'payment_method', 'transaction_ref', 'notes']
        widgets = {
            'paid_amount':     forms.NumberInput(attrs={'class': _INPUT, 'step': '0.01', 'min': '0.01'}),
            'payment_date':    forms.DateInput(attrs={'class': _INPUT, 'type': 'date'}),
            'payment_method':  forms.Select(attrs={'class': _SELECT}),
            'transaction_ref': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Ref / cheque no.'}),
            'notes':           forms.Textarea(attrs={'class': _INPUT, 'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_date'].initial = timezone.localdate()


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
        ).order_by('first_name', 'last_name')


class SalaryMonthFilterForm(forms.Form):
    month = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'class': _INPUT, 'type': 'month'}),
        label='Month',
    )
