from django.db.models.signals import post_save
from django.dispatch import receiver

from appointment_api.models import DoctorProfile

from .models import User


@receiver(post_save, sender=User)
def create_doctor_profile(sender, instance, created, **kwargs):
    if instance.is_doctor:
        DoctorProfile.objects.get_or_create(
            user=instance,
            defaults={
                "experience_years": 0,
                "specialization": "",
            },
        )
