from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from django.contrib.auth import authenticate
from .serializers import UserSignupSerializer, UserLoginSerializer
from .models import CustomUser
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests


def get_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class SignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            tokens = get_tokens(user)
            return Response(tokens, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            tokens = get_tokens(user)
            return Response(tokens)
        return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class GoogleLoginAPIView(APIView):
    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"error": "No token provided"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            idinfo = id_token.verify_oauth2_token(
                token,
                google_requests.Request(),
                settings.GOOGLE_CLIENT_ID
            )

            if not idinfo.get("email_verified", False):
                return Response({"error": "Email not verified by Google"}, status=status.HTTP_400_BAD_REQUEST)

            email = idinfo["email"]
            name = idinfo.get("name", "") or email.split("@")[0]

            user, created = CustomUser.objects.get_or_create(email=email)

            if created:
                base_username = name
                counter = 1
                while CustomUser.objects.filter(username=base_username).exists():
                    base_username = f"{name}{counter}"
                    counter += 1
                user.username = base_username
                user.save()

            tokens = get_tokens(user)
            return Response({
                "access": tokens["access"],
                "refresh": tokens["refresh"],
                "email": user.email,
                "username": user.username,
                "is_new": created,
            })

        except ValueError:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)
