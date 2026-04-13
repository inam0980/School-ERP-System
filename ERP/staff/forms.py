from django import forms
from django.contrib.auth import get_user_model

from core.models import Subject, Section, AcademicYear
from .models import StaffProfile, TeacherAssignment, VacationRequest, MOEApproval

User = get_user_model()

_INPUT = 'w-full border border-slate-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-primary/30 focus:border-primary'


def _apply_classes(form):
    for field in form.fields.values():
        widget = field.widget
        if not isinstance(widget, (forms.CheckboxInput, forms.ClearableFileInput,
                                   forms.CheckboxSelectMultiple)):
            widget.attrs.setdefault('class', _INPUT)


# ──────────────────────────────────────────────────────────────────────────────
# STAFF PROFILE
# ──────────────────────────────────────────────────────────────────────────────

class StaffProfileForm(forms.ModelForm):
    class Meta:
        model  = StaffProfile
        exclude = ['created_at', 'updated_at']
        widgets = {
            'join_date':    forms.DateInput(attrs={'type': 'date'}),
            'iqama_expiry': forms.DateInput(attrs={'type': 'date'}),
            'notes':        forms.Textarea(attrs={'rows': 3}),
            'subjects_taught': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = (
            User.objects.exclude(role='PARENT')
                        .filter(is_active=True)
                        .order_by('full_name')
        )
        self.fields['subjects_taught'].queryset = Subject.objects.filter(is_active=True)
        _apply_classes(self)


# ──────────────────────────────────────────────────────────────────────────────
# TEACHER ASSIGNMENT
# ──────────────────────────────────────────────────────────────────────────────

class TeacherAssignmentForm(forms.ModelForm):
    class Meta:
        model  = TeacherAssignment
        fields = ['teacher', 'subject', 'section', 'academic_year']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['teacher'].queryset = User.objects.filter(
            role='TEACHER', is_active=True).order_by('full_name')
        self.fields['subject'].queryset = Subject.objects.filter(
            is_active=True).select_related('grade', 'division')
        self.fields['section'].queryset = Section.objects.select_related('grade')
        self.fields['academic_year'].queryset = AcademicYear.objects.all()
        current = AcademicYear.objects.filter(is_current=True).first()
        if current:
            self.fields['academic_year'].initial = current.pk
        _apply_classes(self)


# ──────────────────────────────────────────────────────────────────────────────
# VACATION REQUEST
# ──────────────────────────────────────────────────────────────────────────────

class VacationRequestForm(forms.ModelForm):
    class Meta:
        model  = VacationRequest
        fields = ['from_date', 'to_date', 'vacation_type', 'reason']
        widgets = {
            'from_date': forms.DateInput(attrs={'type': 'date'}),
            'to_date':   forms.DateInput(attrs={'type': 'date'}),
            'reason':    forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_classes(self)

    def clean(self):
        cd = super().clean()
        f  = cd.get('from_date')
        t  = cd.get('to_date')
        if f and t and t < f:
            raise forms.ValidationError("End date must be on or after the start date.")
        return cd


class VacationApprovalForm(forms.Form):
    action = forms.ChoiceField(
        choices=[('APPROVED', 'Approve'), ('REJECTED', 'Reject')],
        widget=forms.RadioSelect,
        label='Decision',
    )
    rejection_reason = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3}),
        required=False,
        label='Rejection Reason (required when rejecting)',
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_classes(self)

    def clean(self):
        cd = super().clean()
        if cd.get('action') == 'REJECTED' and not cd.get('rejection_reason', '').strip():
            raise forms.ValidationError("Please provide a reason for rejection.")
        return cd


# ──────────────────────────────────────────────────────────────────────────────
# MOE APPROVAL
# ──────────────────────────────────────────────────────────────────────────────

class MOEApprovalForm(forms.ModelForm):
    class Meta:
        model  = MOEApproval
        fields = ['staff', 'approval_type', 'status', 'reference_number',
                  'file', 'issue_date', 'expiry_date', 'notes']
        widgets = {
            'issue_date':  forms.DateInput(attrs={'type': 'date'}),
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
            'notes':       forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['staff'].queryset = (
            User.objects.exclude(role='PARENT').filter(is_active=True).order_by('full_name')
        )
        _apply_classes(self)


# ──────────────────────────────────────────────────────────────────────────────
# STAFF FILTER
# ──────────────────────────────────────────────────────────────────────────────

class StaffFilterForm(forms.Form):
    q = forms.CharField(
        required=False, label='Search',
        widget=forms.TextInput(attrs={'placeholder': 'Name or employee ID…'}),
    )
    department = forms.ChoiceField(
        required=False,
        choices=[('', 'All Departments')] + StaffProfile.DEPARTMENT_CHOICES,
    )
    designation = forms.ChoiceField(
        required=False,
        choices=[('', 'All Designations')] + StaffProfile.DESIGNATION_CHOICES,
    )
    contract_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All Contract Types'),
                 ('SAUDI', 'Saudi National'),
                 ('FOREIGN', 'Foreign')],
    )
    role = forms.ChoiceField(
        required=False,
        choices=[('', 'All Roles'),
                 ('TEACHER', 'Teacher'),
                 ('ACCOUNTANT', 'Accountant'),
                 ('STAFF', 'Staff'),
                 ('ADMIN', 'Admin')],
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _apply_classes(self)
