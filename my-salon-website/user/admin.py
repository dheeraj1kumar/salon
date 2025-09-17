from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, OTP

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("phone", "email", "name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("Personal info", {"fields": ("name", "email")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone", "password1", "password2", "is_staff", "is_active")}
        ),
    )
    search_fields = ("phone", "email", "name")
    ordering = ("phone",)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(OTP)