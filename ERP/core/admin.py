from django.contrib import admin
from .models import AcademicYear, Division, Grade, Section, Subject


@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display  = ('name', 'start_date', 'end_date', 'is_current')
    list_filter   = ('is_current',)
    search_fields = ('name',)


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display  = ('name', 'curriculum_type', 'is_active')
    list_filter   = ('is_active',)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display  = ('name', 'division', 'order')
    list_filter   = ('division',)
    search_fields = ('name',)


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display  = ('name', 'grade', 'class_teacher', 'capacity')
    list_filter   = ('grade__division',)
    search_fields = ('name',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display  = ('name', 'code', 'grade', 'division', 'is_active')
    list_filter   = ('division', 'is_active')
    search_fields = ('name', 'code')
