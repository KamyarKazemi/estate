from django.db import IntegrityError
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.cache import cache
from accounts.otp import *
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthService:

    @staticmethod
    def complete_registration(data):

        token = data["registration_token"]

        phone_number = cache.get(otp_session_key(token))

        if not phone_number:
            raise ValueError("Registration Failed")

        try:
            user = User.objects.create_user(
                phone_number=phone_number,
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                role=data['role'],
                password=data['password'],
            )
        except IntegrityError:
            raise ValueError("Registration Failed")

        cache.delete(otp_session_key(token))

        refresh = RefreshToken.for_user(user)

        return {
            "detail": "Registration successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

