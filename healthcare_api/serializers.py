from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import DoctorProfile, Appointment

User = get_user_model()

# -----------------------------
# Register Serializer
# -----------------------------
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}   # 👈 this makes it hidden in the browsable API
    )
    password_confirmation = serializers.CharField(
        write_only=True,
        style={'input_type': 'password'}   # 👈 same here
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "password_confirmation"]

    def create(self, validated_data):
        password = validated_data.pop("password")
        password_confirmation = validated_data.pop("password_confirmation")

        if password != password_confirmation:
            raise serializers.ValidationError({"password": "Passwords must match."})

        user = User(**validated_data)
        user.set_password(password)  # hash password
        user.is_doctor = False
        user.save()
        return user


# -----------------------------
# User Serializer (for responses)
# -----------------------------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username", "email", "is_doctor"]


# -----------------------------
# Doctor Profile Serializer
# -----------------------------
class DoctorProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = DoctorProfile
        fields = ["id", "user", "specialization", "experience_years", "available_days", "available_time_slots"]


# -----------------------------
# Appointment Serializer
# -----------------------------
class AppointmentSerializer(serializers.ModelSerializer):
    patient = UserSerializer(read_only=True)
    doctor = DoctorProfileSerializer(read_only=True)

    class Meta:
        model = Appointment
        fields = ["id", "patient", "doctor", "date", "time", "status", "created_at"]



