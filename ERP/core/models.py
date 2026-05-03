from django.db import models
from django.conf import settings


class AcademicYear(models.Model):
    name       = models.CharField(max_length=20, unique=True, help_text="e.g. 2024-25")
    start_date = models.DateField()
    end_date   = models.DateField()
    is_current = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-start_date']
        verbose_name = 'Academic Year'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.is_current:
            AcademicYear.objects.exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)


class Division(models.Model):
    AMERICAN   = 'AMERICAN'
    BRITISH    = 'BRITISH'
    FRENCH     = 'FRENCH'
    HOME_STUDY = 'HOME_STUDY'

    NAME_CHOICES = [
        (AMERICAN,   'American'),
        (BRITISH,    'British'),
        (FRENCH,     'French'),
        (HOME_STUDY, 'Home Study'),
    ]
    CURRICULUM_CHOICES = [
        (AMERICAN,   'American Common Core'),
        (BRITISH,    'British National Curriculum'),
        (FRENCH,     'French National Curriculum'),
        (HOME_STUDY, 'Home Study Programme'),
    ]

    name            = models.CharField(max_length=20, choices=NAME_CHOICES, unique=True)
    curriculum_type = models.CharField(max_length=20, choices=CURRICULUM_CHOICES)
    is_active       = models.BooleanField(default=True)
    created_at      = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.get_name_display()


class Grade(models.Model):
    name      = models.CharField(max_length=50, help_text="e.g. Grade 1, KG1")
    division  = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='grades')
    order     = models.PositiveSmallIntegerField(default=0, help_text="Display order (lower = first)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['division', 'order', 'name']
        unique_together = ['name', 'division']
        verbose_name = 'Grade'

    def __str__(self):
        return f"{self.name} — {self.division}"


class Section(models.Model):
    name          = models.CharField(max_length=10, help_text="e.g. A, B, C")
    grade         = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='sections')
    class_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='sections_taught',
        limit_choices_to={'role': 'TEACHER'},
    )
    capacity   = models.PositiveSmallIntegerField(default=30)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['grade', 'name']
        unique_together = ['name', 'grade']
        verbose_name = 'Section'

    def __str__(self):
        return f"{self.grade} / Section {self.name}"


class Subject(models.Model):
    name      = models.CharField(max_length=100)
    code      = models.CharField(max_length=20, unique=True, help_text="e.g. MATH-G1-AM")
    grade     = models.ForeignKey(Grade, on_delete=models.CASCADE, related_name='subjects')
    division  = models.ForeignKey(Division, on_delete=models.CASCADE, related_name='subjects')
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['division', 'grade', 'name']
        unique_together = ['name', 'grade']
        verbose_name = 'Subject'

    def __str__(self):
        return f"{self.name} ({self.grade})"


class Board(models.Model):
    """External examination board (e.g. CBSE, IGCSE, SAT, etc.)."""
    name       = models.CharField(max_length=100, unique=True,
                                  help_text="e.g. CBSE, IGCSE, SAT, British Board")
    short_code = models.CharField(max_length=20, blank=True,
                                  help_text="Short abbreviation, e.g. CBSE")
    is_active  = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Exam Board'
        verbose_name_plural = 'Exam Boards'

    def __str__(self):
        return self.name

