from django.contrib import admin

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, DoctorProfile, Appointment  

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "is_doctor", "is_staff", "is_superuser")

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "specialization", "experience_years", "available_days", "available_time_slots")

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "date", "time", "status", "created_at")




# Register your models here.
