from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User
    list_display = (
        "email",
        "username",
        "is_staff",
        "is_superuser",
        "is_doctor",
        "is_patient",
    )
    list_filter = ("is_staff", "is_superuser", "is_doctor", "is_patient")
    search_fields = ("email", "username")
    ordering = ("email",)
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        (
            "Permissions",
            {"fields": ("is_staff", "is_superuser", "is_doctor", "is_patient")},
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


# Register your models here.
