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
    RETURNING = 'RETURNING'
    ENROLLMENT_TYPES = [
        (NEW,       'New Student / طالب جديد'),
        (TRANSFER,  'Transfer / منقول'),
        (RETURNING, 'Returning / عائد'),
    ]

    # ── Identity ──────────────────────────────────────────────────────
    student_id   = models.CharField(max_length=20, unique=True, editable=False)
    full_name    = models.CharField(max_length=200, verbose_name="Full Name (English)")
    arabic_name  = models.CharField(max_length=200, verbose_name="الاسم الكامل (عربي)")
    dob          = models.DateField(verbose_name="Date of Birth / تاريخ الميلاد")
    gender       = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Gender / الجنس")
    nationality  = models.CharField(max_length=100, verbose_name="Nationality / الجنسية")
    national_id  = models.CharField(max_length=50, blank=True, verbose_name="National ID / الهوية الوطنية")

    # ── Academic ──────────────────────────────────────────────────────
    division      = models.ForeignKey(Division,     on_delete=models.PROTECT, related_name='students', verbose_name="Division / القسم")
    grade         = models.ForeignKey(Grade,        on_delete=models.PROTECT, related_name='students', verbose_name="Grade / الصف")
    section       = models.ForeignKey(Section,      on_delete=models.PROTECT, related_name='students', verbose_name="Section / الفصل")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT, related_name='students', verbose_name="Academic Year / السنة الدراسية")
    roll_number   = models.CharField(max_length=10, blank=True, verbose_name="Roll No. / رقم السجل")

    # ── Guardian ──────────────────────────────────────────────────────
    father_name     = models.CharField(max_length=200, blank=True, verbose_name="Father's Name / اسم الأب")
    arabic_father   = models.CharField(max_length=200, blank=True, verbose_name="اسم الأب (عربي)")
    mother_name     = models.CharField(max_length=200, blank=True, verbose_name="Mother's Name / اسم الأم")
    arabic_mother   = models.CharField(max_length=200, blank=True, verbose_name="اسم الأم (عربي)")
    guardian_phone  = models.CharField(max_length=20,  blank=True, verbose_name="Guardian Phone / هاتف ولي الأمر")
    guardian_email  = models.EmailField(blank=True, verbose_name="Guardian Email / بريد ولي الأمر")
    guardian_phone2 = models.CharField(max_length=20, blank=True, verbose_name="Alt. Phone / هاتف بديل")

    # ── Address ───────────────────────────────────────────────────────
    address         = models.TextField(blank=True, verbose_name="Address / العنوان")
    arabic_address  = models.TextField(blank=True, verbose_name="العنوان (عربي)")

    # ── Status & Admission ────────────────────────────────────────────
    enrollment_type = models.CharField(max_length=15, choices=ENROLLMENT_TYPES, default=NEW, verbose_name="Enrollment Type / نوع القيد")
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
    def age(self):
        from datetime import date
        today = date.today()
        return today.year - self.dob.year - (
            (today.month, today.day) < (self.dob.month, self.dob.day)
        )


class StudentDocument(models.Model):
    PASSPORT     = 'PASSPORT'
    NATIONAL_ID  = 'NATIONAL_ID'
    BIRTH_CERT   = 'BIRTH_CERT'
    TRANSFER_CERT = 'TRANSFER_CERT'
    PHOTO        = 'PHOTO'
    OTHER        = 'OTHER'

    DOC_TYPES = [
        (PASSPORT,      'Passport / جواز السفر'),
        (NATIONAL_ID,   'National ID / الهوية الوطنية'),
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
