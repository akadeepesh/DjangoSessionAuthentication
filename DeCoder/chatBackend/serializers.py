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



#----------------------------------------------------------1---------------------------------------------------------------#
# from rest_framework import serializers
# from django.contrib.auth import get_user_model, authenticate

# UserModel = get_user_model()

# class UserRegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserModel
#         fields = '__all__'
#     def create(self, clean_data):
#         user_obj = UserModel.objects.create_user(email=clean_data['email'], password=clean_data['password'], first_name=clean_data['first_name'], last_name=clean_data['last_name'])
#         user_obj.first_name = clean_data['first_name']
#         user_obj.last_name = clean_data['last_name']
#         user_obj.save()
#         return user_obj

# class UserLoginSerializer(serializers.Serializer):
#     email = serializers.EmailField()
#     password = serializers.CharField()
#     def check_user(self, clean_data):
#         user = authenticate(email=clean_data['email'], password=clean_data['password'])
#         if not user:
#             raise serializers.ValidationError('user not found')
#         return user

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = UserModel
#         fields = ('email', 'first_name', 'last_name')
