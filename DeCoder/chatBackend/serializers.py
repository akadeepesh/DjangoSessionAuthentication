from rest_framework import serializers
from .models import User
import re


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        password = attrs.get("password")

        if len(password) < 8:
            raise serializers.ValidationError(
                "Password should be at least 8 characters"
            )
        elif not re.search("[a-z]", password):
            raise serializers.ValidationError(
                "Password should contain lowercase characters"
            )
        elif not re.search("[A-Z]", password):
            raise serializers.ValidationError(
                "Password should contain uppercase characters"
            )
        elif not re.search("[0-9]", password):
            raise serializers.ValidationError("Password should have at least a number")
        elif not re.search("[_@$]", password):
            raise serializers.ValidationError(
                "Password should contain a special character"
            )
        else:
            return attrs

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)  # type: ignore


class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ["email", "password"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name")
