from django.shortcuts import render
from .models import UserProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer,LoginSerializer,CurrentUserSerilizer,LogoutSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class Register(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("✅ Register API called")
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "User Registered ",
                    "username" : serializer.data["username"],
                    "email" : serializer.data["email"]
                }, status=status.HTTP_201_CREATED
                )
        print(serializer.errors)
        return Response({
            "errors" : serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):

    permission_classes = [AllowAny]

    def post(self, request):

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():

            return Response(
                {
                    "message": "Login Successful",
                    "username": serializer.validated_data["username"],
                    "access": serializer.validated_data["access"],
                    "refresh": serializer.validated_data["refresh"],
                    "role": serializer.validated_data["role"],
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {
                "errors": serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class CurrentUser(APIView):


    def get(self, request):
        print("Reached CurrentUser view")
        print(request.user)
        user = request.user

        data = {
            "username" : user.username,
            "email" : user.email,
            "role" : user.profile.role
        }

        serilizer = CurrentUserSerilizer(data)
        return Response(serilizer.data, status=status.HTTP_200_OK)
    


class Logout(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = LogoutSerializer(data=request.data)

        if serializer.is_valid():

            try:
                refresh_token = serializer.validated_data["refresh"]

                token = RefreshToken(refresh_token)

                token.blacklist()

                return Response(
                    {
                        "message": "Logout Successful"
                    },
                    status=status.HTTP_200_OK
                )

            except Exception:

                return Response(
                    {
                        "error": "Invalid Refresh Token"
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)