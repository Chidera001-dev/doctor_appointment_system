from django.db import models
from django.conf import settings  
from django.contrib.auth.models import AbstractUser


# Custom User Model
class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)


    def __str__(self):
        return self.username


# Doctor Profile
class DoctorProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,   
        on_delete=models.CASCADE,
        related_name="doctor_profile"
    )
    specialization = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField()
    available_days = models.CharField(max_length=100)  # e.g. "Mon, Wed, Fri"
    available_time_slots = models.CharField(max_length=100)  # e.g. "10AM-2PM"

    def __str__(self):
        return f"Dr. {self.user.username} - {self.specialization}"


# Appointment Model
class Appointment(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
    )

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,     # ✅ use settings.AUTH_USER_MODEL
        on_delete=models.CASCADE,
        related_name="appointments"
    )
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
        related_name="appointments"
    )
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment: {self.patient.username} with {self.doctor.user.username} on {self.date}"





# Create your models here.
