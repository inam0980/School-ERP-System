from django import forms
from core.models import Grade, Section, Division, AcademicYear, StudyMode
from .models import Student, StudentDocument, Sibling, AuthorizedPickup

COUNTRY_CHOICES = [('', '----------')] + [(c, c) for c in [
    'Saudi Arabia', 'Afghanistan', 'Albania', 'Algeria', 'Andorra', 'Angola',
    'Antigua and Barbuda', 'Argentina', 'Armenia', 'Australia', 'Austria',
    'Azerbaijan', 'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus',
    'Belgium', 'Belize', 'Benin', 'Bhutan', 'Bolivia', 'Bosnia and Herzegovina',
    'Botswana', 'Brazil', 'Brunei', 'Bulgaria', 'Burkina Faso', 'Burundi',
    'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 'Central African Republic',
    'Chad', 'Chile', 'China', 'Colombia', 'Comoros', 'Congo', 'Costa Rica',
    'Croatia', 'Cuba', 'Cyprus', 'Czech Republic', 'Denmark', 'Djibouti',
    'Dominica', 'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador',
    'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 'Ethiopia', 'Fiji',
    'Finland', 'France', 'Gabon', 'Gambia', 'Georgia', 'Germany', 'Ghana',
    'Greece', 'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana',
    'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India', 'Indonesia', 'Iran',
    'Iraq', 'Ireland', 'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan',
    'Kazakhstan', 'Kenya', 'Kiribati', 'Kuwait', 'Kyrgyzstan', 'Laos', 'Latvia',
    'Lebanon', 'Lesotho', 'Liberia', 'Libya', 'Liechtenstein', 'Lithuania',
    'Luxembourg', 'Madagascar', 'Malawi', 'Malaysia', 'Maldives', 'Mali',
    'Malta', 'Marshall Islands', 'Mauritania', 'Mauritius', 'Mexico',
    'Micronesia', 'Moldova', 'Monaco', 'Mongolia', 'Montenegro', 'Morocco',
    'Mozambique', 'Myanmar', 'Namibia', 'Nauru', 'Nepal', 'Netherlands',
    'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'North Korea',
    'North Macedonia', 'Norway', 'Oman', 'Pakistan', 'Palau', 'Palestine',
    'Panama', 'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 'Poland',
    'Portugal', 'Qatar', 'Romania', 'Russia', 'Rwanda', 'Saint Kitts and Nevis',
    'Saint Lucia', 'Saint Vincent and the Grenadines', 'Samoa', 'San Marino',
    'Sao Tome and Principe', 'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone',
    'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 'Somalia',
    'South Africa', 'South Korea', 'South Sudan', 'Spain', 'Sri Lanka',
    'Sudan', 'Suriname', 'Sweden', 'Switzerland', 'Syria', 'Taiwan',
    'Tajikistan', 'Tanzania', 'Thailand', 'Timor-Leste', 'Togo', 'Tonga',
    'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Turkmenistan', 'Tuvalu',
    'Uganda', 'Ukraine', 'United Arab Emirates', 'United Kingdom',
    'United States', 'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela',
    'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe',
]]

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
            'enrollment_type', 'study_mode', 'fee_category', 'admission_date', 'previous_school', 'is_active',
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
            'fee_category':              forms.Select(attrs={'class': _INPUT}),
            'enrollment_type':           forms.Select(attrs={'class': _INPUT, 'id': 'id_enrollment_type'}),
            'study_mode':                forms.Select(attrs={'class': _INPUT, 'id': 'id_study_mode'}),
            'is_active':       forms.CheckboxInput(attrs={'class': _CHECK}),
            'photo':           forms.FileInput(attrs={'class': _FILE, 'accept': 'image/*'}),
            'religion':        forms.Select(attrs={'class': _INPUT}),
            'nationality':         forms.Select(attrs={'class': _INPUT}),
            'father_nationality':  forms.Select(attrs={'class': _INPUT}),
            'mother_nationality':  forms.Select(attrs={'class': _INPUT}),
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
        # Only active study modes are selectable; field optional at the form level
        self.fields['study_mode'].queryset    = StudyMode.objects.filter(is_active=True)
        self.fields['study_mode'].required    = False
        self.fields['study_mode'].empty_label = '— Select Study Mode / اختر نمط الدراسة —'
        # Iqama / national ID fields: exactly 10 digits
        self.fields['iqama_number'].required = True
        for fname, placeholder in (
            ('iqama_number',       'Enter 10-digit Iqama number'),
            ('father_national_id', 'Enter 10-digit ID / Iqama number'),
            ('mother_national_id', 'Enter 10-digit ID / Iqama number'),
        ):
            self.fields[fname].widget.attrs.update({
                'maxlength': '10',
                'inputmode': 'numeric',
                'autocomplete': 'off',
                'placeholder': placeholder,
            })
        # Nationality dropdowns
        for fname in ('nationality', 'father_nationality', 'mother_nationality'):
            self.fields[fname].widget.choices = COUNTRY_CHOICES
        # Default current academic year
        current = AcademicYear.objects.filter(is_current=True).first()
        if current and not self.instance.pk:
            self.fields['academic_year'].initial = current

    def _validate_10digit(self, field_name, label):
        val = self.cleaned_data.get(field_name, '').strip()
        if val:
            if not val.isdigit():
                raise forms.ValidationError(f'{label} must contain digits only — no letters or spaces.')
            if len(val) != 10:
                raise forms.ValidationError(
                    f'{label} must be exactly 10 digits (you entered {len(val)}).'
                )
        return val

    def clean_iqama_number(self):
        return self._validate_10digit('iqama_number', 'Iqama number')

    def clean_father_national_id(self):
        return self._validate_10digit('father_national_id', 'Father ID / Iqama number')

    def clean_mother_national_id(self):
        return self._validate_10digit('mother_national_id', 'Mother ID / Iqama number')

    def clean_photo(self):
        f = self.cleaned_data.get('photo')
        _validate_image(f)
        return f

    def clean(self):
        cleaned = super().clean()
        enrollment_type = cleaned.get('enrollment_type')
        study_mode      = cleaned.get('study_mode')
        # Study Mode is required whenever an enrollment type is selected
        if enrollment_type and not study_mode:
            self.add_error('study_mode',
                           'Please select a Study Mode for this student.')
        return cleaned


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
