from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, DoctorProfile, Appointment  

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "is_doctor", "is_staff", "is_superuser")
    
    # Add this to show is_doctor field in the edit form
    fieldsets = UserAdmin.fieldsets + (
        ('Doctor Status', {'fields': ('is_doctor',)}),
    )
    
    # Add this to show is_doctor when creating new user in admin
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Doctor Status', {'fields': ('is_doctor',)}),
    )
    
    def save_model(self, request, obj, form, change):
        """Override save to create DoctorProfile when is_doctor is set to True"""
        # Check if this is an existing user being edited
        was_doctor = False
        if change:
            try:
                original_user = User.objects.get(pk=obj.pk)
                was_doctor = original_user.is_doctor
            except User.DoesNotExist:
                was_doctor = False
        
        # Save the user first
        super().save_model(request, obj, form, change)
        
        # Create DoctorProfile if is_doctor was set to True
        if obj.is_doctor and not was_doctor:
            DoctorProfile.objects.get_or_create(
                user=obj,
                defaults={
                    'specialization': 'General Medicine',
                    'experience_years': 0,
                    'available_days': 'Mon, Tue, Wed, Thu, Fri',
                    'available_time_slots': '9AM-5PM'
                }
            )
        # Delete DoctorProfile if is_doctor was set to False
        elif not obj.is_doctor and was_doctor:
            DoctorProfile.objects.filter(user=obj).delete()

@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "specialization", "experience_years", "available_days", "available_time_slots")

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ("patient", "doctor", "date", "time", "status", "created_at")




# Register your models here.
