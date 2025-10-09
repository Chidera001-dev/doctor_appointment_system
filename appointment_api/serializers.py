import datetime
from rest_framework import serializers
from .models import Appointment, DoctorProfile
from authentication.models import User 


class DoctorProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorProfile
        fields = "__all__"

    def validate_user(self, value):
        if not value:
            raise serializers.ValidationError("A valid user ID must be provided.")
        return value


class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.StringRelatedField(read_only=True)
    doctor = serializers.StringRelatedField(read_only=True)

    
    doctor_id = serializers.CharField(write_only=True)

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
        doctor_uuid = attrs.get("doctor_id")
        date = attrs.get("date")
        time = attrs.get("time")

        # ---- find the doctor profile from UUID ----
        try:
            doctor_user = User.objects.get(id=doctor_uuid, is_doctor=True)
            doctor = DoctorProfile.objects.get(user=doctor_user)
            attrs["doctor"] = doctor
        except User.DoesNotExist:
            raise serializers.ValidationError({"doctor_id": "Doctor user not found."})
        except DoctorProfile.DoesNotExist:
            raise serializers.ValidationError({"doctor_id": "Doctor profile not found."})

        # ---- validate availability ----
        available_days = [d.strip().lower() for d in doctor.available_days.split(",")]
        weekday = date.strftime("%a").lower()

        if weekday not in available_days:
            raise serializers.ValidationError(
                {"date": f"Doctor is not available on {date.strftime('%A')}."}
            )

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
        validated_data["patient"] = request.user
        validated_data.pop("doctor_id", None) 
        return super().create(validated_data)
