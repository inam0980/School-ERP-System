from django.contrib import admin
from .models import Student, StudentDocument, Sibling, AuthorizedPickup


class DocumentInline(admin.TabularInline):
    model  = StudentDocument
    extra  = 0
    fields = ('doc_type', 'file', 'description', 'uploaded_at')
    readonly_fields = ('uploaded_at',)


class SiblingInline(admin.TabularInline):
    model  = Sibling
    extra  = 1
    fields = ('full_name', 'relation', 'dob', 'current_school', 'educational_level')


class AuthorizedPickupInline(admin.TabularInline):
    model  = AuthorizedPickup
    extra  = 1
    fields = ('full_name', 'relation', 'phone')


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display   = ('student_id', 'full_name', 'arabic_name', 'grade', 'section', 'division', 'is_active')
    list_filter    = ('division', 'grade', 'gender', 'is_active', 'enrollment_type')
    search_fields  = ('full_name', 'arabic_name', 'student_id', 'guardian_phone')
    ordering       = ('grade', 'section', 'full_name')
    readonly_fields = ('student_id', 'created_at', 'updated_at')
    inlines        = [DocumentInline, SiblingInline, AuthorizedPickupInline]
    fieldsets = (
        ('Identity / الهوية',       {'fields': ('student_id', 'full_name', 'arabic_name', 'dob', 'gender', 'nationality', 'national_id', 'iqama_number', 'passport_number', 'religion', 'birth_place', 'photo')}),
        ('Academic / أكاديمي',     {'fields': ('division', 'grade', 'section', 'academic_year', 'roll_number')}),
        ('Father Information / معلومات الأب', {'fields': (
            'father_name', 'arabic_father', 'father_nationality', 'father_family_book_no',
            'father_national_id', 'father_occupation', 'father_employer', 'father_business_phone',
            'father_mobile', 'father_work_address', 'father_email', 'father_home_phone',
            'father_home_address', 'father_employed_at_school', 'father_school_job',
        )}),
        ('Mother Information / معلومات الأم', {'fields': (
            'mother_name', 'arabic_mother', 'mother_nationality', 'mother_family_book_no',
            'mother_national_id', 'mother_occupation', 'mother_employer', 'mother_business_phone',
            'mother_mobile', 'mother_work_address', 'mother_email', 'mother_home_phone',
            'mother_home_address', 'mother_employed_at_school', 'mother_school_job',
        )}),
        ('General Contact / جهة الاتصال', {'fields': ('guardian_phone', 'guardian_phone2', 'guardian_email')}),
        ('Address / العنوان',      {'fields': ('address', 'arabic_address')}),
        ('Status / الحالة',        {'fields': ('enrollment_type', 'admission_date', 'previous_school', 'is_active', 'created_by', 'created_at', 'updated_at')}),
    )


@admin.register(StudentDocument)
class StudentDocumentAdmin(admin.ModelAdmin):
    list_display  = ('student', 'doc_type', 'filename', 'uploaded_at', 'uploaded_by')
    list_filter   = ('doc_type',)
    search_fields = ('student__full_name', 'student__student_id')
    readonly_fields = ('uploaded_at',)


@admin.register(Sibling)
class SiblingAdmin(admin.ModelAdmin):
    list_display  = ('student', 'full_name', 'relation', 'dob', 'current_school', 'educational_level')
    list_filter   = ('relation',)
    search_fields = ('student__full_name', 'student__student_id', 'full_name')


@admin.register(AuthorizedPickup)
class AuthorizedPickupAdmin(admin.ModelAdmin):
    list_display  = ('student', 'full_name', 'relation', 'phone')
    search_fields = ('student__full_name', 'student__student_id', 'full_name', 'phone')
