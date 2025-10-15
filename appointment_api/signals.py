from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import pre_save
from django.dispatch import receiver

from .models import Appointment


@receiver(pre_save, sender=Appointment)
def send_appointment_status_email(sender, instance, **kwargs):
    """Send email when doctor confirms or cancels an appointment"""

    if not instance.pk:
        return

    try:
        previous = Appointment.objects.get(pk=instance.pk)
    except Appointment.DoesNotExist:
        return

    # Trigger only if status has changed
    if previous.status != instance.status:
        patient = instance.patient
        doctor = instance.doctor.user
        subject = "Your Appointment Status Has Been Updated"

        if instance.status == "confirmed":
            message = f"""
            Hello {patient.username},

            Good news! Your appointment with Dr. {doctor.username} 
            on {instance.date} at {instance.time} has been CONFIRMED.

            Please make sure to arrive on time.

            Regards,
            Hospital Management Team
            """

        elif instance.status == "cancelled":
            message = f"""
            Hello {patient.username},

            Your appointment with Dr. {doctor.username} 
            on {instance.date} at {instance.time} has been CANCELLED.

            We’re sorry for the inconvenience. 
            You can reschedule your appointment through the hospital portal.

            Regards,
            Hospital Management Team
            """

        else:
            return

        # Send the email via Mailtrap SMTP
        send_mail(
            subject,
            message.strip(),
            settings.DEFAULT_FROM_EMAIL,
            [patient.email],
            fail_silently=False,
        )
