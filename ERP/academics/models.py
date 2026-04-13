from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from core.models import AcademicYear, Division, Grade, Section, Subject
from students.models import Student


# ──────────────────────────────────────────────────────────────────────────────
# EXAM TYPE  (Quiz / Assignment / MidTerm / Final)
# ──────────────────────────────────────────────────────────────────────────────

class ExamType(models.Model):
    name              = models.CharField(max_length=50, unique=True, help_text="e.g. Quiz, MidTerm, Final")
    weight_percentage = models.PositiveSmallIntegerField(
        default=100,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        help_text="Weight of this exam type in the overall grade (1-100)",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Exam Type'

    def __str__(self):
        return f"{self.name} ({self.weight_percentage}%)"


# ──────────────────────────────────────────────────────────────────────────────
# EXAM
# ──────────────────────────────────────────────────────────────────────────────

TERM_CHOICES = [
    ('T1', 'Term 1'),
    ('T2', 'Term 2'),
    ('T3', 'Term 3'),
    ('FI', 'Final'),
]


class Exam(models.Model):
    name          = models.CharField(max_length=200)
    exam_type     = models.ForeignKey(ExamType, on_delete=models.PROTECT, related_name='exams')
    subject       = models.ForeignKey(Subject,  on_delete=models.PROTECT, related_name='exams')
    section       = models.ForeignKey(Section,  on_delete=models.PROTECT, related_name='exams')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT, related_name='exams')
    term          = models.CharField(max_length=2, choices=TERM_CHOICES, default='T1')
    date          = models.DateField()
    total_marks   = models.PositiveSmallIntegerField(default=100)
    created_by    = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True,
        related_name='exams_created',
    )
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', 'name']
        verbose_name = 'Exam'

    def __str__(self):
        return f"{self.name} — {self.subject} ({self.section})"


# ──────────────────────────────────────────────────────────────────────────────
# MARK  (per student per exam)
# ──────────────────────────────────────────────────────────────────────────────

MARK_STATUS = [
    ('draft',     'Draft'),
    ('submitted', 'Submitted'),
    ('approved',  'Approved'),
]


class Mark(models.Model):
    student        = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='marks')
    exam           = models.ForeignKey(Exam,    on_delete=models.CASCADE, related_name='marks')
    obtained_marks = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    is_absent      = models.BooleanField(default=False)
    status         = models.CharField(max_length=10, choices=MARK_STATUS, default='draft')
    remarks        = models.CharField(max_length=200, blank=True)
    entered_by     = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='marks_entered',
    )
    approved_by    = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL, null=True, blank=True,
        related_name='marks_approved',
    )
    approved_at    = models.DateTimeField(null=True, blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'exam']
        ordering = ['student__full_name']
        verbose_name = 'Mark'

    def __str__(self):
        return f"{self.student} — {self.exam} — {self.obtained_marks}"

    # ── Auto-computed helpers ─────────────────────────────────────────
    def get_percentage(self):
        if self.is_absent or self.obtained_marks is None:
            return None
        return round(float(self.obtained_marks) / self.exam.total_marks * 100, 1)

    def get_letter_grade(self):
        pct = self.get_percentage()
        if pct is None:
            return 'AB'
        if pct >= 90: return 'A+'
        if pct >= 85: return 'A'
        if pct >= 80: return 'B+'
        if pct >= 75: return 'B'
        if pct >= 70: return 'C+'
        if pct >= 65: return 'C'
        if pct >= 60: return 'D'
        return 'F'

    def get_gpa_points(self):
        grade = self.get_letter_grade()
        mapping = {
            'A+': 4.0, 'A': 4.0, 'B+': 3.5, 'B': 3.0,
            'C+': 2.5, 'C': 2.0, 'D': 1.0, 'F': 0.0, 'AB': 0.0,
        }
        return mapping.get(grade, 0.0)

    def is_passed(self):
        pct = self.get_percentage()
        return pct is not None and pct >= 60


# ──────────────────────────────────────────────────────────────────────────────
# GRADE CONFIG (passing mark threshold per grade)
# ──────────────────────────────────────────────────────────────────────────────

class GradeConfig(models.Model):
    GPA_AMERICAN = 'AMERICAN'
    GPA_BRITISH  = 'BRITISH'
    GPA_FRENCH   = 'FRENCH'
    GPA_SCALE_CHOICES = [
        (GPA_AMERICAN, 'American (4.0 GPA)'),
        (GPA_BRITISH,  'British (A*-U)'),
        (GPA_FRENCH,   'French (20-point)'),
    ]

    grade         = models.OneToOneField(Grade, on_delete=models.CASCADE, related_name='config')
    passing_marks = models.PositiveSmallIntegerField(default=60, help_text="Passing percentage (1-100)")
    gpa_scale     = models.CharField(max_length=10, choices=GPA_SCALE_CHOICES, default=GPA_AMERICAN)

    class Meta:
        verbose_name = 'Grade Config'

    def __str__(self):
        return f"Config: {self.grade} — Pass ≥ {self.passing_marks}%"


# ──────────────────────────────────────────────────────────────────────────────
# REPORT CARD
# ──────────────────────────────────────────────────────────────────────────────

class ReportCard(models.Model):
    student       = models.ForeignKey(Student,     on_delete=models.CASCADE, related_name='report_cards')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.PROTECT, related_name='report_cards')
    term          = models.CharField(max_length=2,  choices=TERM_CHOICES)
    generated_at  = models.DateTimeField(auto_now=True)
    pdf_file      = models.FileField(upload_to='report_cards/', blank=True, null=True)

    class Meta:
        unique_together = ['student', 'academic_year', 'term']
        ordering = ['-generated_at']
        verbose_name = 'Report Card'

    def __str__(self):
        return f"{self.student} — {self.academic_year} {self.get_term_display()}"

