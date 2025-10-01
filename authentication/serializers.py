from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField
from .models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=25)
    email = serializers.EmailField(max_length=80)
    phone_number = PhoneNumberField(allow_null=False, allow_blank=False)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'password']
        extra_kwargs = {
            'password': {'write_only': True},  # ✅ Never expose password in response
        }

    # Validate unique fields
    def validate(self, attrs):
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError({"username": "User with this username already exists"})

        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "User with this email already exists"})

        if User.objects.filter(phone_number=attrs['phone_number']).exists():
            raise serializers.ValidationError({"phone_number": "User with this phone number already exists"})

        return attrs

    # Create user with hashed password
    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            phone_number=validated_data['phone_number'],
            is_doctor=False  # 🔒 Force new users to be normal users (patients)
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# ✅ Serializer for returning user data (useful in responses)
class UserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone_number', 'is_doctor']
        
