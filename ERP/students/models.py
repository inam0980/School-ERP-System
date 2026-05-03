import uuid
from django.db import models
from django.conf import settings
from core.models import AcademicYear, Division, Grade, Section


def student_photo_path(instance, filename):
    ext = filename.rsplit('.', 1)[-1]
    return f"students/photos/{instance.student_id}.{ext}"


def student_doc_path(instance, filename):
    return f"students/documents/{instance.student.student_id}/{filename}"


class Student(models.Model):
    # ── Gender & Enrollment choices ───────────────────────────────────
    MALE   = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [(MALE, 'Male / ذكر'), (FEMALE, 'Female / أنثى')]

    NEW       = 'NEW'
    TRANSFER  = 'TRANSFER'
    REGULAR   = 'REGULAR'
    ENROLLMENT_TYPES = [
        (NEW,       'New Student / طالب جديد'),
        (TRANSFER,  'Transfer / منقول'),
        (REGULAR,   'Regular (Continuing) / مستمر'),
    ]

    # ── Fee category choices ──────────────────────────────────────────
    FEE_CAT_NEW     = 'new'
    FEE_CAT_REGULAR = 'regular'
    FEE_CAT_OTHER   = 'other'
    FEE_CATEGORY_CHOICES = [
        (FEE_CAT_NEW,     'New'),
        (FEE_CAT_REGULAR, 'Regular'),
        (FEE_CAT_OTHER,   'Other'),
    ]

    # ── ID type choices ───────────────────────────────────────────────
    NATIONAL_ID_TYPE = 'NATIONAL_ID'
    IQAMA            = 'IQAMA'
    PASSPORT_ID      = 'PASSPORT'
    ID_TYPE_CHOICES  = [
        (NATIONAL_ID_TYPE, 'National ID / هوية وطنية'),
        (IQAMA,            'Iqama / إقامة'),
        (PASSPORT_ID,      'Passport / جواز السفر'),
    ]

    # ── Identity ──────────────────────────────────────────────────────
    student_id   = models.CharField(max_length=20, unique=True, editable=False)
    full_name    = models.CharField(max_length=200, verbose_name="Full Name (English)")
    arabic_name  = models.CharField(max_length=200, verbose_name="الاسم الكامل (عربي)")
    dob          = models.DateField(verbose_name="Date of Birth / تاريخ الميلاد")
    gender       = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Gender / الجنس")
    nationality  = models.CharField(max_length=100, verbose_name="Nationality / الجنسية")
    id_type      = models.CharField(
        max_length=15, choices=ID_TYPE_CHOICES, default=NATIONAL_ID_TYPE,
        verbose_name="ID Type / نوع الهوية",
        help_text="Saudi students: National ID (هوية وطنية)  ·  Residents: Iqama (إقامة)  ·  Others: Passport"
    )
    national_id  = models.CharField(max_length=50, blank=True, verbose_name="ID Number / رقم الهوية")
    iqama_number = models.CharField(max_length=50, blank=True, verbose_name="Iqama Number / رقم الإقامة")
    passport_number = models.CharField(max_length=50, blank=True, verbose_name="Passport Number / رقم جواز السفر")
    religion     = models.CharField(max_length=100, blank=True, verbose_name="Religion / الديانة")
    birth_place  = models.CharField(max_length=200, blank=True, verbose_name="Birth Place / مكان الميلاد")

    # ── Academic ──────────────────────────────────────────────────────
    division      = models.ForeignKey(Division,     on_delete=models.PROTECT, related_name='students', verbose_name="Division / القسم")
    grade         = models.ForeignKey(Grade,        on_delete=models.PROTECT, related_name='students', verbose_name="Grade / الصف")
    section       = models.ForeignKey(Section,      on_delete=models.PROTECT, related_name='students', verbose_name="Section / الفصل")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT, related_name='students', verbose_name="Academic Year / السنة الدراسية")
    roll_number   = models.CharField(max_length=10, blank=True, verbose_name="Roll No. / رقم السجل")

    # ── Father Information ────────────────────────────────────────────
    YES = 'YES'
    NO  = 'NO'
    YES_NO_CHOICES = [(YES, 'Yes'), (NO, 'No')]

    father_name              = models.CharField(max_length=200, blank=True, verbose_name="Father Full Name (Latin) / الاسم بالكامل")
    arabic_father            = models.CharField(max_length=200, blank=True, verbose_name="Father Full Name (Arabic) / الاسم بالكامل")
    father_nationality       = models.CharField(max_length=100, blank=True, verbose_name="Father Nationality / الجنسية")
    father_family_book_no    = models.CharField(max_length=50, blank=True, verbose_name="Father Family Book No. (Saudi) / رقم دفتر العائلة")
    father_national_id       = models.CharField(max_length=50, blank=True, verbose_name="Father ID/Iqama Number / رقم الإقامة للجنسية الأجنبية")
    father_occupation        = models.CharField(max_length=200, blank=True, verbose_name="Father Occupation / المهنة")
    father_employer          = models.CharField(max_length=200, blank=True, verbose_name="Father Company Name / اسم الشركة")
    father_business_phone    = models.CharField(max_length=20, blank=True, verbose_name="Father Business Phone / رقم هاتف العمل")
    father_mobile            = models.CharField(max_length=20, blank=True, verbose_name="Father Mobile / رقم الجوال")
    father_work_address      = models.CharField(max_length=300, blank=True, verbose_name="Father Work Address / عنوان العمل")
    father_email             = models.EmailField(blank=True, verbose_name="Father Email / البريد الإلكتروني")
    father_home_phone        = models.CharField(max_length=20, blank=True, verbose_name="Father Home Phone / رقم هاتف المنزل")
    father_home_address      = models.TextField(blank=True, verbose_name="Father Home Address / عنوان المنزل")
    father_employed_at_school = models.CharField(
        max_length=3, choices=YES_NO_CHOICES, blank=True,
        verbose_name="Father Employed at Al Kawthar? / الوالد عضو في هيئة التدريس؟"
    )
    father_school_job        = models.CharField(max_length=200, blank=True, verbose_name="Father School Job / تحديد الوظيفة")

    # ── Mother Information ────────────────────────────────────────────
    mother_name              = models.CharField(max_length=200, blank=True, verbose_name="Mother Full Name (Latin) / الاسم بالكامل")
    arabic_mother            = models.CharField(max_length=200, blank=True, verbose_name="Mother Full Name (Arabic) / الاسم بالكامل")
    mother_nationality       = models.CharField(max_length=100, blank=True, verbose_name="Mother Nationality / الجنسية")
    mother_family_book_no    = models.CharField(max_length=50, blank=True, verbose_name="Mother Family Book No. (Saudi) / رقم دفتر العائلة")
    mother_national_id       = models.CharField(max_length=50, blank=True, verbose_name="Mother ID/Iqama Number / رقم الإقامة للجنسية الأجنبية")
    mother_occupation        = models.CharField(max_length=200, blank=True, verbose_name="Mother Occupation / المهنة")
    mother_employer          = models.CharField(max_length=200, blank=True, verbose_name="Mother Company Name / اسم الشركة")
    mother_business_phone    = models.CharField(max_length=20, blank=True, verbose_name="Mother Business Phone / رقم هاتف العمل")
    mother_mobile            = models.CharField(max_length=20, blank=True, verbose_name="Mother Mobile / رقم الجوال")
    mother_work_address      = models.CharField(max_length=300, blank=True, verbose_name="Mother Work Address / عنوان العمل")
    mother_email             = models.EmailField(blank=True, verbose_name="Mother Email / البريد الإلكتروني")
    mother_home_phone        = models.CharField(max_length=20, blank=True, verbose_name="Mother Home Phone / رقم هاتف المنزل")
    mother_home_address      = models.TextField(blank=True, verbose_name="Mother Home Address / عنوان المنزل")
    mother_employed_at_school = models.CharField(
        max_length=3, choices=YES_NO_CHOICES, blank=True,
        verbose_name="Mother Employed at Al Kawthar? / الأم عضو في هيئة التدريس؟"
    )
    mother_school_job        = models.CharField(max_length=200, blank=True, verbose_name="Mother School Job / تحديد الوظيفة")

    # ── Legacy contact (kept for backward compat) ─────────────────────
    guardian_phone  = models.CharField(max_length=20, blank=True, verbose_name="Guardian Phone / هاتف ولي الأمر")
    guardian_email  = models.EmailField(blank=True, verbose_name="Guardian Email / بريد ولي الأمر")
    guardian_phone2 = models.CharField(max_length=20, blank=True, verbose_name="Alt. Phone / هاتف بديل")

    # ── Address ───────────────────────────────────────────────────────
    address         = models.TextField(blank=True, verbose_name="Address / العنوان")
    arabic_address  = models.TextField(blank=True, verbose_name="العنوان (عربي)")

    # ── Status & Admission ────────────────────────────────────────────
    enrollment_type = models.CharField(max_length=15, choices=ENROLLMENT_TYPES, default=NEW, verbose_name="Enrollment Type / نوع القيد")
    fee_category    = models.CharField(
        max_length=10, choices=FEE_CATEGORY_CHOICES, default=FEE_CAT_REGULAR,
        verbose_name="Fee Category",
        help_text="Determines which fee structure applies to this student"
    )
    admission_date  = models.DateField(verbose_name="Admission Date / تاريخ القبول")
    is_active       = models.BooleanField(default=True, verbose_name="Active / نشط")
    previous_school = models.CharField(max_length=200, blank=True, verbose_name="Previous School / المدرسة السابقة")

    # ── Photo ─────────────────────────────────────────────────────────
    photo = models.ImageField(upload_to=student_photo_path, blank=True, null=True,
                              verbose_name="Photo / الصورة")

    # ── Timestamps ───────────────────────────────────────────────────
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='students_added'
    )
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['grade', 'section', 'full_name']
        verbose_name = 'Student / طالب'
        indexes = [
            models.Index(fields=['section'], name='student_section_idx'),
            models.Index(fields=['grade', 'section'], name='student_grade_section_idx'),
            models.Index(fields=['academic_year', 'is_active'], name='student_year_active_idx'),
            models.Index(fields=['student_id'], name='student_id_idx'),
        ]

    def __str__(self):
        return f"[{self.student_id}] {self.full_name}"

    def save(self, *args, **kwargs):
        if not self.student_id:
            year = self.academic_year.name.replace('-', '')[:4]
            div  = self.division.name[:2].upper()
            uid  = str(uuid.uuid4().int)[:5]
            self.student_id = f"AKS-{year}-{div}-{uid}"
        super().save(*args, **kwargs)

    @property
    def is_saudi(self):
        """True if the student holds a Saudi National ID (not Iqama/Passport)."""
        return self.id_type == self.NATIONAL_ID_TYPE

    @property
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.dob.year - (
            (today.month, today.day) < (self.dob.month, self.dob.day)
        )


class StudentDocument(models.Model):
    PASSPORT     = 'PASSPORT'
    NATIONAL_ID  = 'NATIONAL_ID'
    IQAMA        = 'IQAMA'
    BIRTH_CERT   = 'BIRTH_CERT'
    TRANSFER_CERT = 'TRANSFER_CERT'
    PHOTO        = 'PHOTO'
    OTHER        = 'OTHER'

    DOC_TYPES = [
        (NATIONAL_ID,   'National ID / الهوية الوطنية'),
        (IQAMA,         'Iqama / إقامة'),
        (PASSPORT,      'Passport / جواز السفر'),
        (BIRTH_CERT,    'Birth Certificate / شهادة الميلاد'),
        (TRANSFER_CERT, 'Transfer Certificate / شهادة النقل'),
        (PHOTO,         'Photograph / صورة شخصية'),
        (OTHER,         'Other / أخرى'),
    ]

    student     = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='documents')
    doc_type    = models.CharField(max_length=20, choices=DOC_TYPES, verbose_name="Document Type / نوع الوثيقة")
    file        = models.FileField(upload_to=student_doc_path, verbose_name="File / الملف")
    description = models.CharField(max_length=200, blank=True, verbose_name="Notes / ملاحظات")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='documents_uploaded'
    )

    class Meta:
        ordering = ['-uploaded_at']
        verbose_name = 'Student Document / وثيقة الطالب'

    def __str__(self):
        return f"{self.student} — {self.get_doc_type_display()}"

    @property
    def filename(self):
        import os
        return os.path.basename(self.file.name)

    @property
    def ext(self):
        return self.filename.rsplit('.', 1)[-1].lower() if '.' in self.filename else ''


class Sibling(models.Model):
    BROTHER = 'BROTHER'
    SISTER  = 'SISTER'
    RELATION_CHOICES = [
        (BROTHER, 'Brother / أخ'),
        (SISTER,  'Sister / أخت'),
    ]

    student           = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='siblings')
    full_name         = models.CharField(max_length=200, verbose_name="Full Name / الاسم بالكامل")
    relation          = models.CharField(max_length=10, choices=RELATION_CHOICES, verbose_name="Relation / العلاقة")
    dob               = models.DateField(null=True, blank=True, verbose_name="Date of Birth / تاريخ الميلاد")
    current_school    = models.CharField(max_length=200, blank=True, verbose_name="Current School / المدرسة الحالية")
    educational_level = models.CharField(max_length=200, blank=True, verbose_name="Educational Level / المرحلة الدراسية")

    class Meta:
        ordering = ['relation', 'full_name']
        verbose_name = 'Sibling / أخ/أخت'

    def __str__(self):
        return f"{self.student} — {self.get_relation_display()} — {self.full_name}"


class AuthorizedPickup(models.Model):
    student  = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='authorized_pickups')
    full_name = models.CharField(max_length=200, verbose_name="Full Name / الاسم بالكامل")
    relation  = models.CharField(max_length=100, verbose_name="Relation / العلاقة")
    phone     = models.CharField(max_length=20, verbose_name="Phone / رقم الهاتف")

    class Meta:
        ordering = ['full_name']
        verbose_name = 'Authorized Pickup Person / شخص مُصرَّح له باصطحاب الطالب'

    def __str__(self):
        return f"{self.student} — {self.full_name} ({self.relation})"
