from django.contrib import admin
from .models import ExamType, Exam, Mark, GradeConfig, ReportCard


class MarkInline(admin.TabularInline):
    model  = Mark
    extra  = 0
    fields = ('student', 'obtained_marks', 'is_absent', 'status', 'remarks')
    readonly_fields = ('student',)


@admin.register(ExamType)
class ExamTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'weight_percentage')


@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display  = ('name', 'subject', 'section', 'term', 'date', 'total_marks', 'academic_year')
    list_filter   = ('term', 'academic_year', 'section')
    search_fields = ('name', 'subject__name')
    inlines       = [MarkInline]


@admin.register(Mark)
class MarkAdmin(admin.ModelAdmin):
    list_display  = ('student', 'exam', 'obtained_marks', 'is_absent', 'status')
    list_filter   = ('status', 'is_absent', 'exam__term')
    search_fields = ('student__full_name', 'student__student_id')


@admin.register(GradeConfig)
class GradeConfigAdmin(admin.ModelAdmin):
    list_display = ('grade', 'passing_marks', 'gpa_scale')


@admin.register(ReportCard)
class ReportCardAdmin(admin.ModelAdmin):
    list_display = ('student', 'academic_year', 'term', 'generated_at')
    list_filter  = ('term', 'academic_year')
