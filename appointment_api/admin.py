from django.contrib import admin
from .models import DoctorProfile, Appointment


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "specialization",
        "experience_years",
        "available_days",
        "available_time_slots",
    )
    search_fields = ("user__username", "specialization")
    list_filter = ("specialization", "experience_years")


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "patient",
        "doctor",
        "date",
        "time",
        "status",
        "created_at",
    )
    search_fields = ("patient__username", "doctor__user__username")
    list_filter = ("status", "date")
    ordering = ("-created_at",)





# Register your models here.
