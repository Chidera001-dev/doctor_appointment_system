from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User


# Input serializer (for registration + update)
class UserSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True) 

    username = serializers.CharField(
        max_length=25, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    email = serializers.EmailField(
        max_length=80, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    phone_number = PhoneNumberField(
        allow_null=False,
        allow_blank=False,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        min_length=8,
        write_only=True,
        required=True,  
        style={"input_type": "password"},
    )

    class Meta:
        model = User
        fields = ["id", "username", "email", "phone_number", "password"]

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            phone_number=validated_data["phone_number"],
            is_doctor=False,
        )
        user.set_password(validated_data["password"])  # hashes password
        user.save()
        return user

    def update(self, instance, validated_data):
        # Handle password updates separately
        password = validated_data.pop("password", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


# Output serializer (safe response)
class UserCreationSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)  

    class Meta:
        model = User
        fields = ["id", "username", "email", "phone_number"]
