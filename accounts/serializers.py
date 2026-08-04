from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import UserProfile



class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def create(self, validated_data):

        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"]
        )

        return user

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    access = serializers.CharField(read_only=True)
    refresh = serializers.CharField(read_only=True)

    def validate(self, attrs):
        user = authenticate(
            username=attrs["username"],
            password=attrs["password"]
        
        )
        if user is None:
            raise serializers.ValidationError(
                "Invalid username or password."
            )
        refresh = RefreshToken.for_user(user)

        return {
            "username": user.username,
            "role": user.profile.role,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }


class CurrentUserSerilizer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()
    
    role = serializers.CharField()

class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    
class UserListSerializer(serializers.ModelSerializer):


    role = serializers.CharField(source="profile.role")

    class Meta:
        model = User
        fields = ["id", "username", "email", "role"]

class UpdateUserSerializer(serializers.ModelSerializer):


    class Meta:
        model = UserProfile
        fields = ["role"]

     












   