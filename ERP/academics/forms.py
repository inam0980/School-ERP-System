from django import forms
from django.contrib.auth import get_user_model
from .models import ExamType, Exam, Mark, GradeConfig
from core.models import Subject, Section, AcademicYear, Grade, Division

User = get_user_model()

_INPUT   = ('w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm text-slate-700 '
            'focus:outline-none focus:ring-2 focus:ring-[#1e3a5f]/30 focus:border-[#1e3a5f] '
            'transition bg-white')
_CHECK   = 'w-4 h-4 text-[#1e3a5f] rounded border-slate-300 cursor-pointer'
_SMALL   = ('w-full px-2 py-1.5 border border-slate-200 rounded text-sm text-slate-700 '
            'focus:outline-none focus:ring-1 focus:ring-[#1e3a5f]/30 bg-white')


class ExamTypeForm(forms.ModelForm):
    class Meta:
        model  = ExamType
        fields = ['name', 'weight_percentage']
        widgets = {
            'name':              forms.TextInput(attrs={'class': _INPUT}),
            'weight_percentage': forms.NumberInput(attrs={'class': _INPUT, 'min': 1, 'max': 100}),
        }


class ExamForm(forms.ModelForm):
    class Meta:
        model  = Exam
        fields = ['name', 'exam_type', 'subject', 'section', 'academic_year', 'term', 'date', 'total_marks']
        widgets = {
            'name':          forms.TextInput(attrs={'class': _INPUT}),
            'exam_type':     forms.Select(attrs={'class': _INPUT}),
            'subject':       forms.Select(attrs={'class': _INPUT}),
            'section':       forms.Select(attrs={'class': _INPUT}),
            'academic_year': forms.Select(attrs={'class': _INPUT}),
            'term':          forms.Select(attrs={'class': _INPUT}),
            'date':          forms.DateInput(attrs={'type': 'date', 'class': _INPUT}),
            'total_marks':   forms.NumberInput(attrs={'class': _INPUT, 'min': 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['academic_year'].queryset = AcademicYear.objects.all().order_by('-start_date')


class MarksEntryFilterForm(forms.Form):
    """Filter used on the marks entry page to select an exam."""
    subject = forms.ModelChoiceField(
        queryset=Subject.objects.filter(is_active=True),
        required=False,
        empty_label='Select Subject',
        widget=forms.Select(attrs={'class': _INPUT}),
    )
    section = forms.ModelChoiceField(
        queryset=Section.objects.all(),
        required=False,
        empty_label='Select Section',
        widget=forms.Select(attrs={'class': _INPUT}),
    )
    exam = forms.ModelChoiceField(
        queryset=Exam.objects.none(),
        required=False,
        empty_label='Select Exam',
        widget=forms.Select(attrs={'class': _INPUT}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'section' in self.data and 'subject' in self.data:
            try:
                sec_id = int(self.data.get('section'))
                sub_id = int(self.data.get('subject'))
                self.fields['exam'].queryset = Exam.objects.filter(
                    section_id=sec_id, subject_id=sub_id
                ).order_by('-date')
            except (ValueError, TypeError):
                pass


class GradeConfigForm(forms.ModelForm):
    class Meta:
        model  = GradeConfig
        fields = ['grade', 'passing_marks', 'gpa_scale']
        widgets = {
            'grade':         forms.Select(attrs={'class': _INPUT}),
            'passing_marks': forms.NumberInput(attrs={'class': _INPUT, 'min': 1, 'max': 100}),
            'gpa_scale':     forms.Select(attrs={'class': _INPUT}),
        }


class ReportCardFilterForm(forms.Form):
    """Filter for generating / viewing report cards."""
    section = forms.ModelChoiceField(
        queryset=Section.objects.select_related('grade', 'grade__division').all(),
        required=True,
        empty_label='Select Section',
        widget=forms.Select(attrs={'class': _INPUT}),
    )
    academic_year = forms.ModelChoiceField(
        queryset=AcademicYear.objects.all().order_by('-start_date'),
        required=True,
        empty_label='Select Year',
        widget=forms.Select(attrs={'class': _INPUT}),
    )
    term = forms.ChoiceField(
        choices=[('', 'Select Term'), ('T1', 'Term 1'), ('T2', 'Term 2'), ('T3', 'Term 3'), ('FI', 'Final')],
        required=True,
        widget=forms.Select(attrs={'class': _INPUT}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Try to default to current academic year
        try:
            current = AcademicYear.objects.get(is_current=True)
            self.fields['academic_year'].initial = current.pk
        except AcademicYear.DoesNotExist:
            pass
