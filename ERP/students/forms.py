from django import forms
from core.models import Grade, Section, Division, AcademicYear
from .models import Student, StudentDocument, Sibling, AuthorizedPickup

_INPUT  = ('w-full px-3 py-2.5 border border-slate-200 rounded-lg text-sm text-slate-700 '
           'focus:outline-none focus:ring-2 focus:ring-[#1e3a5f]/30 focus:border-[#1e3a5f] '
           'transition bg-white')
_CHECK  = 'w-4 h-4 text-[#1e3a5f] rounded border-slate-300 cursor-pointer'
_FILE   = ('block w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 '
           'file:rounded-lg file:border-0 file:text-sm file:font-medium '
           'file:bg-[#1e3a5f] file:text-white hover:file:bg-[#2a5298] file:cursor-pointer')

_ALLOWED_IMAGE_EXTS   = {'.jpg', '.jpeg', '.png', '.webp'}
_ALLOWED_DOC_EXTS     = {'.pdf', '.jpg', '.jpeg', '.png', '.doc', '.docx'}
_MAX_PHOTO_BYTES      = 5 * 1024 * 1024    # 5 MB
_MAX_DOC_BYTES        = 10 * 1024 * 1024   # 10 MB


def _validate_image(f):
    """Reject non-image files and files that exceed the size limit."""
    import os
    if f:
        ext = os.path.splitext(f.name)[1].lower()
        if ext not in _ALLOWED_IMAGE_EXTS:
            raise forms.ValidationError(
                f"Only {', '.join(_ALLOWED_IMAGE_EXTS)} files are allowed."
            )
        if f.size > _MAX_PHOTO_BYTES:
            raise forms.ValidationError("Photo must not exceed 5 MB.")


def _validate_document(f):
    """Reject disallowed document types and oversized files."""
    import os
    if f:
        ext = os.path.splitext(f.name)[1].lower()
        if ext not in _ALLOWED_DOC_EXTS:
            raise forms.ValidationError(
                f"Only {', '.join(_ALLOWED_DOC_EXTS)} files are allowed."
            )
        if f.size > _MAX_DOC_BYTES:
            raise forms.ValidationError("Document must not exceed 10 MB.")


class StudentForm(forms.ModelForm):
    class Meta:
        model  = Student
        fields = [
            # Identity
            'full_name', 'arabic_name', 'dob', 'gender', 'nationality', 'national_id',
            'iqama_number', 'passport_number', 'religion', 'birth_place',
            # Academic
            'division', 'grade', 'section', 'academic_year', 'roll_number',
            # Father
            'father_name', 'arabic_father', 'father_nationality', 'father_family_book_no',
            'father_national_id', 'father_occupation', 'father_employer', 'father_business_phone',
            'father_mobile', 'father_work_address', 'father_email', 'father_home_phone',
            'father_home_address', 'father_employed_at_school', 'father_school_job',
            # Mother
            'mother_name', 'arabic_mother', 'mother_nationality', 'mother_family_book_no',
            'mother_national_id', 'mother_occupation', 'mother_employer', 'mother_business_phone',
            'mother_mobile', 'mother_work_address', 'mother_email', 'mother_home_phone',
            'mother_home_address', 'mother_employed_at_school', 'mother_school_job',
            # Legacy contact
            'guardian_phone', 'guardian_phone2', 'guardian_email',
            # Address
            'address', 'arabic_address',
            # Status
            'enrollment_type', 'admission_date', 'previous_school', 'is_active',
            # Photo
            'photo',
        ]

        widgets = {
            'dob':             forms.DateInput(attrs={'type': 'date', 'class': _INPUT}),
            'admission_date':  forms.DateInput(attrs={'type': 'date', 'class': _INPUT}),
            'address':         forms.Textarea(attrs={'rows': 2, 'class': _INPUT}),
            'arabic_address':  forms.Textarea(attrs={'rows': 2, 'class': _INPUT, 'dir': 'rtl'}),
            'arabic_name':     forms.TextInput(attrs={'dir': 'rtl', 'class': _INPUT}),
            'arabic_father':   forms.TextInput(attrs={'dir': 'rtl', 'class': _INPUT}),
            'arabic_mother':   forms.TextInput(attrs={'dir': 'rtl', 'class': _INPUT}),
            'father_home_address': forms.Textarea(attrs={'rows': 2, 'class': _INPUT}),
            'mother_home_address': forms.Textarea(attrs={'rows': 2, 'class': _INPUT}),
            'father_employed_at_school': forms.Select(attrs={'class': _INPUT}),
            'mother_employed_at_school': forms.Select(attrs={'class': _INPUT}),
            'is_active':       forms.CheckboxInput(attrs={'class': _CHECK}),
            'photo':           forms.FileInput(attrs={'class': _FILE, 'accept': 'image/*'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            w = field.widget
            if isinstance(w, (forms.CheckboxInput, forms.FileInput)):
                pass  # already handled
            elif 'class' not in w.attrs:
                w.attrs['class'] = _INPUT
        # Dynamic queryset — all; JS will filter division→grade→section
        self.fields['grade'].queryset   = Grade.objects.select_related('division').all()
        self.fields['section'].queryset = Section.objects.select_related('grade__division').all()
        # Default current academic year
        current = AcademicYear.objects.filter(is_current=True).first()
        if current and not self.instance.pk:
            self.fields['academic_year'].initial = current

    def clean_photo(self):
        f = self.cleaned_data.get('photo')
        _validate_image(f)
        return f


class DocumentUploadForm(forms.ModelForm):
    class Meta:
        model  = StudentDocument
        fields = ['doc_type', 'file', 'description']
        widgets = {
            'doc_type':    forms.Select(attrs={'class': _INPUT}),
            'description': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Optional notes / ملاحظات اختيارية'}),
            'file':        forms.FileInput(attrs={'class': _FILE}),
        }

    def clean_file(self):
        f = self.cleaned_data.get('file')
        _validate_document(f)
        return f


class SiblingForm(forms.ModelForm):
    class Meta:
        model  = Sibling
        fields = ['full_name', 'relation', 'dob', 'current_school', 'educational_level']
        widgets = {
            'full_name':         forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Full Name / الاسم بالكامل'}),
            'relation':          forms.Select(attrs={'class': _INPUT}),
            'dob':               forms.DateInput(attrs={'type': 'date', 'class': _INPUT}),
            'current_school':    forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Current School / المدرسة الحالية'}),
            'educational_level': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Educational Level / المرحلة الدراسية'}),
        }


class AuthorizedPickupForm(forms.ModelForm):
    class Meta:
        model  = AuthorizedPickup
        fields = ['full_name', 'relation', 'phone']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Full Name / الاسم بالكامل'}),
            'relation':  forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'e.g. Uncle, Grandmother / العلاقة'}),
            'phone':     forms.TextInput(attrs={'class': _INPUT, 'placeholder': 'Phone Number / رقم الهاتف'}),
        }


class StudentFilterForm(forms.Form):
    q        = forms.CharField(required=False,
                               widget=forms.TextInput(attrs={
                                   'class': _INPUT,
                                   'placeholder': 'Name, ID, or Arabic name / الاسم أو الرقم',
                               }))
    division = forms.ModelChoiceField(queryset=Division.objects.all(), required=False, empty_label="All Divisions",
                                      widget=forms.Select(attrs={'class': _INPUT}))
    grade    = forms.ModelChoiceField(queryset=Grade.objects.all(), required=False, empty_label="All Grades",
                                      widget=forms.Select(attrs={'class': _INPUT}))
    section  = forms.ModelChoiceField(queryset=Section.objects.all(), required=False, empty_label="All Sections",
                                      widget=forms.Select(attrs={'class': _INPUT}))
    gender   = forms.ChoiceField(
        choices=[('', 'All Genders')] + Student.GENDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': _INPUT}),
    )
    is_active = forms.ChoiceField(
        choices=[('', 'All'), ('1', 'Active'), ('0', 'Inactive')],
        required=False,
        widget=forms.Select(attrs={'class': _INPUT}),
    )
    citizenship = forms.ChoiceField(
        choices=[('', 'All'), ('saudi', 'Saudi 🇸🇦'), ('expat', 'Non-Saudi 🌍')],
        required=False,
        widget=forms.Select(attrs={'class': _INPUT}),
    )
