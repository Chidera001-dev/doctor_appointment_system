from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import DoctorProfile, Appointment
from authentication.serializers import UserSerializer  # User serializer for nested info

User = get_user_model()


# -------------------------
# DoctorProfile Serializer
# -------------------------
class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)  # show basic user info

    class Meta:
        model = DoctorProfile
        fields = "__all__"  # id, user, specialization, experience_years, available_days, available_time_slots

# -------------------------
# Appointment Serializer
# -------------------------
class AppointmentSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)   # show patient info
    doctor = DoctorProfileSerializer(read_only=True)  # show doctor info

    # write-only field to assign doctor via ID
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=DoctorProfile.objects.all(),
        source="doctor",
        write_only=True
    )

    class Meta:
        model = Appointment
        fields = [
            "id",
            "patient",
            "doctor",
            "doctor_id",
            "date",
            "time",
            "status",
            "created_at",
        ]
        read_only_fields = ["status", "created_at"]

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["patient"] = request.user  # assign logged-in user as patient
        return super().create(validated_data)
