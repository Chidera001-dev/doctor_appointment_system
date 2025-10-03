import datetime

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

    def validate(self, attrs):
        """
        Custom validation for doctor's available days & time slots.
        """
        doctor = attrs["doctor"]
        date = attrs["date"]
        time = attrs["time"]

        # ---- 1. Check available days ----
        # Example: doctor.available_days = "Mon,Tue,Thu"
        available_days = [d.strip().lower() for d in doctor.available_days.split(",")]
        weekday = date.strftime("%a").lower()  # e.g. "mon"

        if weekday not in available_days:
            raise serializers.ValidationError(
                {"date": f"Doctor is not available on {date.strftime('%A')}."}
            )

        # ---- 2. Check available time slots ----
        # Example: doctor.available_time_slots = "10AM-2PM"
        try:
            start_str, end_str = doctor.available_time_slots.split("-")
            start_time = datetime.datetime.strptime(start_str.strip(), "%I%p").time()
            end_time = datetime.datetime.strptime(end_str.strip(), "%I%p").time()
        except Exception:
            raise serializers.ValidationError(
                {
                    "time": "Doctor's available_time_slots format is invalid. Use '10AM-2PM'."
                }
            )

        if not (start_time <= time <= end_time):
            raise serializers.ValidationError(
                {
                    "time": f"Doctor is only available between {start_time.strftime('%I:%M %p')} and {end_time.strftime('%I:%M %p')}."
                }
            )

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["patient"] = request.user  # assign logged-in user as patient
        return super().create(validated_data)
