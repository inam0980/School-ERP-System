from django.db import models
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from core.models import AcademicYear, Division, Subject, Section


# ──────────────────────────────────────────────────────────────────────────────
# STAFF PROFILE
# ──────────────────────────────────────────────────────────────────────────────

class StaffProfile(models.Model):
    DEPARTMENT_CHOICES = [
        ('ACADEMIC',    'Academic'),
        ('ADMIN',       'Administration'),
        ('FINANCE',     'Finance'),
        ('IT',          'Information Technology'),
        ('OPERATIONS',  'Operations'),
        ('HR',          'Human Resources'),
        ('SECURITY',    'Security'),
        ('TRANSPORT',   'Transport'),
        ('COUNSELING',  'Counseling'),
        ('OTHER',       'Other'),
    ]

    DESIGNATION_CHOICES = [
        ('TEACHER',       'Teacher'),
        ('SENIOR_TEACHER','Senior Teacher'),
        ('HEAD_OF_DEPT',  'Head of Department'),
        ('COORDINATOR',   'Coordinator'),
        ('VICE_PRINCIPAL','Vice Principal'),
        ('PRINCIPAL',     'Principal'),
        ('ACCOUNTANT',    'Accountant'),
        ('HR_OFFICER',    'HR Officer'),
        ('IT_OFFICER',    'IT Officer'),
        ('COUNSELOR',     'Counselor'),
        ('LIBRARIAN',     'Librarian'),
        ('SECURITY_GUARD','Security Guard'),
        ('DRIVER',        'Driver'),
        ('CLERK',         'Clerk'),
        ('OTHER',         'Other'),
    ]

    CONTRACT_SAUDI   = 'SAUDI'
    CONTRACT_FOREIGN = 'FOREIGN'
    CONTRACT_CHOICES = [
        (CONTRACT_SAUDI,   'Saudi National'),
        (CONTRACT_FOREIGN, 'Foreign (Expatriate)'),
    ]

    user                    = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='staff_profile',
    )
    employee_id             = models.CharField(max_length=20, unique=True,
                                               help_text="e.g. EMP-0001")
    designation             = models.CharField(max_length=30, choices=DESIGNATION_CHOICES)
    department              = models.CharField(max_length=20, choices=DEPARTMENT_CHOICES)
    division                = models.ForeignKey(Division, on_delete=models.SET_NULL,
                                                null=True, blank=True,
                                                related_name='staff_profiles')
    join_date               = models.DateField()
    nationality             = models.CharField(max_length=60, default='Saudi')
    iqama_number            = models.CharField(max_length=20, blank=True,
                                               help_text="For foreign employees")
    iqama_expiry            = models.DateField(null=True, blank=True)
    contract_type           = models.CharField(max_length=10, choices=CONTRACT_CHOICES,
                                               default=CONTRACT_FOREIGN)
    phone                   = models.CharField(max_length=20, blank=True)
    emergency_contact_name  = models.CharField(max_length=100, blank=True)
    emergency_contact_phone = models.CharField(max_length=20, blank=True)
    photo                   = models.ImageField(upload_to='staff_photos/',
                                                null=True, blank=True)
    subjects_taught         = models.ManyToManyField(
        Subject, blank=True,
        related_name='teaching_staff',
        help_text="Subjects this staff member is qualified to teach",
    )
    notes                   = models.TextField(blank=True)
    created_at              = models.DateTimeField(auto_now_add=True)
    updated_at              = models.DateTimeField(auto_now=True)

    class Meta:
        ordering     = ['department', 'user__full_name']
        verbose_name = 'Staff Profile'

    def __str__(self):
        return f"{self.user.full_name} ({self.employee_id})"

    @property
    def full_name(self):
        return self.user.full_name

    @property
    def is_iqama_expiring_soon(self):
        """True if iqama expires within 90 days."""
        if not self.iqama_expiry:
            return False
        return self.iqama_expiry <= (timezone.localdate() + timedelta(days=90))


# ──────────────────────────────────────────────────────────────────────────────
# TEACHER ASSIGNMENT  (who teaches which subject in which section / year)
# ──────────────────────────────────────────────────────────────────────────────

class TeacherAssignment(models.Model):
    teacher       = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teaching_assignments',
        limit_choices_to={'role': 'TEACHER'},
    )
    subject       = models.ForeignKey(Subject, on_delete=models.CASCADE,
                                      related_name='teacher_assignments')
    section       = models.ForeignKey(Section, on_delete=models.CASCADE,
                                      related_name='teacher_assignments')
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE,
                                      related_name='teacher_assignments')
    created_at    = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['teacher', 'subject', 'section', 'academic_year']
        ordering        = ['academic_year', 'section', 'subject']
        verbose_name    = 'Teacher Assignment'

    def __str__(self):
        return (f"{self.teacher.full_name} → "
                f"{self.subject.name} / {self.section} ({self.academic_year})")


# ──────────────────────────────────────────────────────────────────────────────
# VACATION REQUEST
# ──────────────────────────────────────────────────────────────────────────────

class VacationRequest(models.Model):
    ANNUAL    = 'ANNUAL'
    SICK      = 'SICK'
    EMERGENCY = 'EMERGENCY'
    HAJJ      = 'HAJJ'
    MATERNITY = 'MATERNITY'
    UNPAID    = 'UNPAID'

    VACATION_TYPE_CHOICES = [
        (ANNUAL,    'Annual Leave'),
        (SICK,      'Sick Leave'),
        (EMERGENCY, 'Emergency Leave'),
        (HAJJ,      'Hajj Leave'),
        (MATERNITY, 'Maternity / Paternity Leave'),
        (UNPAID,    'Unpaid Leave'),
    ]

    PENDING  = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'

    STATUS_CHOICES = [
        (PENDING,  'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]

    staff            = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='vacation_requests',
    )
    from_date        = models.DateField()
    to_date          = models.DateField()
    vacation_type    = models.CharField(max_length=15, choices=VACATION_TYPE_CHOICES,
                                        default=ANNUAL)
    reason           = models.TextField()
    status           = models.CharField(max_length=10, choices=STATUS_CHOICES,
                                        default=PENDING)
    approved_by      = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='vacation_approvals',
    )
    approved_at      = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    created_at       = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering     = ['-created_at']
        verbose_name = 'Vacation Request'

    def __str__(self):
        return (f"{self.staff.full_name} — {self.get_vacation_type_display()} "
                f"({self.from_date} → {self.to_date})")

    @property
    def duration_days(self):
        return (self.to_date - self.from_date).days + 1


# ──────────────────────────────────────────────────────────────────────────────
# MOE / REGULATORY APPROVALS
# ──────────────────────────────────────────────────────────────────────────────

class MOEApproval(models.Model):
    AJEER           = 'AJEER'
    SAUDI_EMP       = 'SAUDI_EMP'
    TEACHER_LICENSE = 'TEACHER_LICENSE'
    IQAMA_RENEWAL   = 'IQAMA_RENEWAL'
    WORK_PERMIT     = 'WORK_PERMIT'
    OTHER           = 'OTHER'

    APPROVAL_TYPE_CHOICES = [
        (AJEER,           'Ajeer Registration'),
        (SAUDI_EMP,       'Saudi Employee Registration'),
        (TEACHER_LICENSE, 'Teacher License (MOE)'),
        (IQAMA_RENEWAL,   'Iqama Renewal'),
        (WORK_PERMIT,     'Work Permit'),
        (OTHER,           'Other'),
    ]

    PENDING   = 'PENDING'
    SUBMITTED = 'SUBMITTED'
    APPROVED  = 'APPROVED'
    REJECTED  = 'REJECTED'
    EXPIRED   = 'EXPIRED'

    STATUS_CHOICES = [
        (PENDING,   'Pending'),
        (SUBMITTED, 'Submitted'),
        (APPROVED,  'Approved'),
        (REJECTED,  'Rejected'),
        (EXPIRED,   'Expired'),
    ]

    staff            = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='moe_approvals',
    )
    approval_type    = models.CharField(max_length=20, choices=APPROVAL_TYPE_CHOICES)
    status           = models.CharField(max_length=10, choices=STATUS_CHOICES,
                                        default=PENDING)
    reference_number = models.CharField(max_length=100, blank=True)
    file             = models.FileField(upload_to='moe_files/', null=True, blank=True)
    issue_date       = models.DateField(null=True, blank=True)
    expiry_date      = models.DateField(null=True, blank=True)
    notes            = models.TextField(blank=True)
    created_by       = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='moe_approvals_created',
    )
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    class Meta:
        ordering     = ['-created_at']
        verbose_name = 'MOE / Regulatory Approval'

    def __str__(self):
        return (f"{self.staff.full_name} — "
                f"{self.get_approval_type_display()} — {self.get_status_display()}")

    @property
    def is_expiring_soon(self):
        """True if approved document expires within 60 days."""
        if not self.expiry_date:
            return False
        return self.expiry_date <= (timezone.localdate() + timedelta(days=60))
