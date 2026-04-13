from django.contrib import admin
from .models import StaffProfile, TeacherAssignment, VacationRequest, MOEApproval


@admin.register(StaffProfile)
class StaffProfileAdmin(admin.ModelAdmin):
    list_display   = ['employee_id', 'user', 'designation', 'department',
                      'contract_type', 'join_date', 'is_iqama_expiring_soon']
    list_filter    = ['department', 'designation', 'contract_type', 'division']
    search_fields  = ['user__full_name', 'employee_id', 'iqama_number']
    filter_horizontal = ['subjects_taught']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(TeacherAssignment)
class TeacherAssignmentAdmin(admin.ModelAdmin):
    list_display  = ['teacher', 'subject', 'section', 'academic_year']
    list_filter   = ['academic_year', 'subject__grade']
    search_fields = ['teacher__full_name', 'subject__name']


@admin.register(VacationRequest)
class VacationRequestAdmin(admin.ModelAdmin):
    list_display  = ['staff', 'vacation_type', 'from_date', 'to_date',
                     'duration_days', 'status', 'approved_by']
    list_filter   = ['status', 'vacation_type']
    search_fields = ['staff__full_name']
    readonly_fields = ['approved_at']


@admin.register(MOEApproval)
class MOEApprovalAdmin(admin.ModelAdmin):
    list_display  = ['staff', 'approval_type', 'status', 'reference_number',
                     'expiry_date', 'is_expiring_soon']
    list_filter   = ['approval_type', 'status']
    search_fields = ['staff__full_name', 'reference_number']
    readonly_fields = ['created_at', 'updated_at']
