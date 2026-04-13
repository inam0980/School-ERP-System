from django import forms
from django.contrib.auth import get_user_model
from .models import AcademicYear, Division, Grade, Section, Subject

User = get_user_model()

# Base Tailwind CSS classes for widgets
_INPUT  = ('w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm text-slate-700 '
           'focus:outline-none focus:ring-2 focus:ring-[#1e3a5f]/30 focus:border-[#1e3a5f] '
           'transition bg-white')
_CHECK  = 'w-4 h-4 text-[#1e3a5f] rounded border-slate-300 cursor-pointer'


class TailwindMixin:
    """Apply Tailwind CSS classes to all form widgets automatically."""
    def apply_tailwind(self):
        for field in self.fields.values():
            w = field.widget
            if isinstance(w, forms.CheckboxInput):
                w.attrs.setdefault('class', _CHECK)
            else:
                w.attrs.setdefault('class', _INPUT)


class AcademicYearForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model  = AcademicYear
        fields = ['name', 'start_date', 'end_date', 'is_current']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': _INPUT}),
            'end_date':   forms.DateInput(attrs={'type': 'date', 'class': _INPUT}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind()


class DivisionForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model  = Division
        fields = ['name', 'curriculum_type', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind()


class GradeForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model  = Grade
        fields = ['name', 'division', 'order']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind()


class SectionForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model  = Section
        fields = ['name', 'grade', 'class_teacher', 'capacity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['class_teacher'].queryset  = User.objects.filter(role='TEACHER', is_active=True)
        self.fields['class_teacher'].required  = False
        self.fields['class_teacher'].empty_label = '— Unassigned —'
        self.apply_tailwind()


class SubjectForm(TailwindMixin, forms.ModelForm):
    class Meta:
        model  = Subject
        fields = ['name', 'code', 'grade', 'division', 'is_active']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_tailwind()
