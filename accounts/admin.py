from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile


# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ('email', 'is_superuser', 'is_active')
    list_filter = ('email', 'is_superuser', 'is_active')
    search_fields = ('email',)
    ordering = ('email',)
    fieldsets = (
        ('authentication', {
            'fields': ('email','password'),
        }),
        ('permissions', {
            'fields': ('is_staff', 'is_active'),
        }),
        ('group permissions', {
            'fields': ('groups', 'user_permissions'),
        }),
        ('important date', {
            'fields': ('last_login',),
        }),

    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email','password1', 'password2', 'is_staff', 'is_active', 'is_superuser'),
        }),
    )

admin.site.register(Profile)
admin.site.register(User, CustomUserAdmin)


