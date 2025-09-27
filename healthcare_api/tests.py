from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import DoctorProfile

User = get_user_model()

class DoctorTests(APITestCase):
    def setUp(self):
        DoctorProfile.objects.all().delete()   # wipe doctors
        User.objects.all().delete()            # wipe users

        # Create a patient user
        self.patient = User.objects.create_user(username="patient1", password="1234")

        # Create a doctor user + doctor profile
        self.doctor_user = User.objects.create_user(username="doc1", password="1234", is_doctor=True)
        self.doctor_profile = DoctorProfile.objects.create(
            user=self.doctor_user,
            specialization="Cardiology",
            experience_years=5
        )

    def test_patient_can_view_doctors(self):
        # Authenticate as patient
        self.client.force_authenticate(user=self.patient)

        # Hit endpoint
        response = self.client.get("/api/doctors/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)   # check count
        self.assertEqual(response.data["results"][0]["specialization"], "Cardiology")





from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from .models import DoctorProfile, Appointment

User = get_user_model()

class AppointmentTests(APITestCase):
    def setUp(self):
        # Patient
        self.patient = User.objects.create_user(username="patient1", password="1234")

        # Doctor + Profile
        self.doctor_user = User.objects.create_user(username="doc1", password="1234", is_doctor=True)
        self.doctor_profile = DoctorProfile.objects.create(
            user=self.doctor_user,
            specialization="Cardiology"
        )

    def test_patient_can_book_appointment(self):
        self.client.force_authenticate(user=self.patient)

        data = {
            "doctor": self.doctor_profile.id,  # <-- check if it's profile.id or user.id in your serializer
            "date": "2025-10-01",
            "time": "10:00:00"
        }
        response = self.client.post("/api/appointments/", data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(Appointment.objects.count(), 1)
        appointment = Appointment.objects.first()
        self.assertEqual(appointment.patient, self.patient)
        self.assertEqual(appointment.doctor, self.doctor_profile)  # <-- adjust if doctor is linked to User



# Create your tests here.
