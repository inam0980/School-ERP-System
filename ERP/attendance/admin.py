from django.contrib import admin
from .models import Attendance, StaffAttendance


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display  = ('student', 'date', 'status', 'marked_by', 'remarks')
    list_filter   = ('status', 'date', 'student__section', 'student__grade', 'student__division')
    search_fields = ('student__full_name', 'student__student_id')
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-date', 'student__full_name')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'student', 'student__grade', 'student__section', 'marked_by'
        )


@admin.register(StaffAttendance)
class StaffAttendanceAdmin(admin.ModelAdmin):
    list_display  = ('staff', 'date', 'status', 'marked_by', 'remarks')
    list_filter   = ('status', 'date')
    search_fields = ('staff__full_name', 'staff__username')
    date_hierarchy = 'date'
    readonly_fields = ('created_at',)
    ordering = ('-date',)
