from django.contrib import admin
from .models import Student, StudentDocument


class DocumentInline(admin.TabularInline):
    model  = StudentDocument
    extra  = 0
    fields = ('doc_type', 'file', 'description', 'uploaded_at')
    readonly_fields = ('uploaded_at',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display   = ('student_id', 'full_name', 'arabic_name', 'grade', 'section', 'division', 'is_active')
    list_filter    = ('division', 'grade', 'gender', 'is_active', 'enrollment_type')
    search_fields  = ('full_name', 'arabic_name', 'student_id', 'guardian_phone')
    ordering       = ('grade', 'section', 'full_name')
    readonly_fields = ('student_id', 'created_at', 'updated_at')
    inlines        = [DocumentInline]
    fieldsets = (
        ('Identity / الهوية',       {'fields': ('student_id', 'full_name', 'arabic_name', 'dob', 'gender', 'nationality', 'national_id', 'photo')}),
        ('Academic / أكاديمي',     {'fields': ('division', 'grade', 'section', 'academic_year', 'roll_number')}),
        ('Guardian / ولي الأمر',   {'fields': ('father_name', 'arabic_father', 'mother_name', 'arabic_mother', 'guardian_phone', 'guardian_phone2', 'guardian_email')}),
        ('Address / العنوان',      {'fields': ('address', 'arabic_address')}),
        ('Status / الحالة',        {'fields': ('enrollment_type', 'admission_date', 'previous_school', 'is_active', 'created_by', 'created_at', 'updated_at')}),
    )


@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):
    list_display  = ('student', 'doc_type', 'filename', 'uploaded_at', 'uploaded_by')
    list_filter   = ('doc_type',)
    search_fields = ('student__full_name', 'student__student_id')
    readonly_fields = ('uploaded_at',)
