from django import forms
from datetime import date
from core.models import Division, Grade, Section

_INPUT = ('w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm text-slate-700 '
          'focus:outline-none focus:ring-2 focus:ring-[#1e3a5f]/30 focus:border-[#1e3a5f] '
          'transition bg-white')


class AttendanceFilterForm(forms.Form):
    """Filter bar used on both Take Attendance and Report pages."""
    division = forms.ModelChoiceField(
        queryset=Division.objects.filter(is_active=True),
        required=False,
        empty_label='All Divisions',
        widget=forms.Select(attrs={'class': _INPUT, 'id': 'id_division'}),
    )
    grade = forms.ModelChoiceField(
        queryset=Grade.objects.none(),
        required=False,
        empty_label='Select Grade',
        widget=forms.Select(attrs={'class': _INPUT, 'id': 'id_grade'}),
    )
    section = forms.ModelChoiceField(
        queryset=Section.objects.none(),
        required=False,
        empty_label='Select Section',
        widget=forms.Select(attrs={'class': _INPUT, 'id': 'id_section'}),
    )
    date = forms.DateField(
        required=False,
        initial=date.today,
        widget=forms.DateInput(attrs={'type': 'date', 'class': _INPUT}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically populate grade/section based on submitted values
        if 'division' in self.data:
            try:
                div_id = int(self.data.get('division'))
                self.fields['grade'].queryset = Grade.objects.filter(division_id=div_id)
            except (ValueError, TypeError):
                pass
        if 'grade' in self.data:
            try:
                grade_id = int(self.data.get('grade'))
                self.fields['section'].queryset = Section.objects.filter(grade_id=grade_id)
            except (ValueError, TypeError):
                pass


class ReportFilterForm(forms.Form):
    """Extended filter for the attendance report page."""
    division = forms.ModelChoiceField(
        queryset=Division.objects.filter(is_active=True),
        required=False,
        empty_label='All Divisions',
        widget=forms.Select(attrs={'class': _INPUT}),
    )
    grade = forms.ModelChoiceField(
        queryset=Grade.objects.all(),
        required=False,
        empty_label='All Grades',
        widget=forms.Select(attrs={'class': _INPUT}),
    )
    section = forms.ModelChoiceField(
        queryset=Section.objects.all(),
        required=False,
        empty_label='All Sections',
        widget=forms.Select(attrs={'class': _INPUT}),
    )
    student_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Search student...'}),
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': _INPUT}),
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date', 'class': _INPUT}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'division' in self.data:
            try:
                div_id = int(self.data.get('division'))
                self.fields['grade'].queryset = Grade.objects.filter(division_id=div_id)
            except (ValueError, TypeError):
                pass
        if 'grade' in self.data:
            try:
                grade_id = int(self.data.get('grade'))
                self.fields['section'].queryset = Section.objects.filter(grade_id=grade_id)
            except (ValueError, TypeError):
                pass
