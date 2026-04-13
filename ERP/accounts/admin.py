from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Division


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display  = ('username', 'full_name', 'email', 'role', 'division', 'is_active')
    list_filter   = ('role', 'division', 'is_active')
    search_fields = ('username', 'email', 'full_name')
    ordering      = ('username',)
    fieldsets = (
        (None,           {'fields': ('username', 'password')}),
        ('Personal',     {'fields': ('full_name', 'email', 'role', 'division')}),
        ('Permissions',  {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'full_name', 'role', 'division', 'password1', 'password2'),
        }),
    )


@admin.register(Division)
class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
