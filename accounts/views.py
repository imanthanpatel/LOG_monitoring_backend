from django.shortcuts import render
from .models import UserProfile
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer,LoginSerializer,CurrentUserSerilizer,LogoutSerializer,UserListSerializer,UpdateUserSerializer
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from .permissions import IsAdmin,IsSOC,IsInvestigator,IsViewer,IsAdminOrSOC
from django.shortcuts import get_object_or_404


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

            except Exception as e:
                    print("========== ERROR ==========")
                    print(type(e))
                    print(e)
                    print("===========================")

                    return Response(
                        {
                            "error": str(e)
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # Get all users
        users=User.objects.all()

        # Serialize them
        serializer = UserListSerializer(users, many=True)


        # Return response
        return Response(serializer.data)

class UpdateUser(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def patch(self, request, id):
        user = get_object_or_404(User, id=id)

        serializer = UpdateUserSerializer(
            user.profile,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()
            return Response({
                "message" : "User Role Updated Successfully",
                "user" : serializer.data
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class DeleteUser(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def delete(self, request, id):

        user = get_object_or_404(User, id=id)

        if request.user == user:
            return Response(
                {
                    "error": "You cannot delete your own account."
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user.delete()

        return Response(
            {
                "message": "User deleted successfully"
            },
            status=status.HTTP_200_OK
        )  