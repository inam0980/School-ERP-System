from django.db import models
from django.conf import settings
from students.models import Student


STATUS_CHOICES = [
    ('P', 'Present'),
    ('A', 'Absent'),
    ('L', 'Late'),
    ('E', 'Excused'),
]

STATUS_COLORS = {
    'P': 'emerald',
    'A': 'red',
    'L': 'amber',
    'E': 'blue',
}


class Attendance(models.Model):
    """Daily student attendance record. One row per student per day."""

    student   = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='attendances',
    )
    date      = models.DateField(db_index=True)
    status    = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='attendances_marked',
    )
    remarks    = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'date']   # prevents duplicates
        ordering = ['-date', 'student__full_name']
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
        indexes = [
            models.Index(fields=['date', 'student'], name='attendance_date_student_idx'),
            models.Index(fields=['student', 'status'], name='attendance_student_status_idx'),
        ]

    def __str__(self):
        return f"{self.student.full_name} — {self.date} — {self.get_status_display()}"

    @property
    def is_present(self):
        return self.status in ('P', 'L')


class StaffAttendance(models.Model):
    """Daily staff/teacher attendance record."""

    staff     = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='staff_attendances',
    )
    date      = models.DateField(db_index=True)
    status    = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P')
    marked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='staff_attendances_marked',
    )
    remarks    = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['staff', 'date']
        ordering = ['-date']
        verbose_name = 'Staff Attendance'
        verbose_name_plural = 'Staff Attendance Records'

    def __str__(self):
        return f"{self.staff.full_name} — {self.date} — {self.get_status_display()}"
