from rest_framework import serializers

from .models import Appointment, DoctorProfile

# DoctorProfile Serializer


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = "__all__"  # includes: id, user, specialization, experience_years, available_days, available_time_slots

    def validate_user(self, value):
        """
        Ensure that the 'user' field is provided when creating a doctor profile.
        """
        if not value:
            raise serializers.ValidationError("A valid user ID must be provided.")
        return value


# Appointment Serializer


class AppointmentSerializer(serializers.ModelSerializer):
    # show patient and doctor info
    patient = serializers.StringRelatedField(read_only=True)
    doctor = serializers.StringRelatedField(read_only=True)

    # write-only field to assign doctor via ID
    doctor_id = serializers.PrimaryKeyRelatedField(
        queryset=DoctorProfile.objects.all(), source="doctor", write_only=True
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
