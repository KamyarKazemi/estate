from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SendOtpSerializer, VerifyOtpSerializer, CompleteRegistrationSerializer
from .otp import *
from .utils import send_otp_code
import json
from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import IntegrityError
from django.shortcuts import get_object_or_404



User = get_user_model()
MAX_OTP_ATTEMPTS = 5



class SendOtpRegisterView(APIView):
    """
    Send Otp with phone_number and save code in redis
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = SendOtpSerializer

    def post(self , request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']

        # checking for repeated phone_number
        if User.objects.filter(phone_number=phone_number).exists():
            return Response({'message':'Phone number already exists'}, status=status.HTTP_400_BAD_REQUEST)

        # check limit of sending otp in exact time
        if cache.get(otp_limit_key(phone_number)):
            return Response({"message" : "Try agin later"} , status=status.HTTP_429_TOO_MANY_REQUESTS)

        code = generate_otp_code()
        session_token = generate_session_token()

        # send OTP
        try:
            send_otp_code(phone_number, code)
        except Exception as e:
            return Response({"message" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # save datas in redis cache
        cache.set(otp_data_key(phone_number), code , timeout=OTP_TTL_SECONDS)
        cache.set(otp_limit_key(phone_number), True , timeout=OTP_RATE_LIMIT_SECONDS)
        cache.set(otp_session_key(session_token), phone_number , timeout=OTP_TTL_SECONDS)

        # delete all attempts for this phone_number
        cache.delete(f"otp_attempts:{phone_number}")

        return Response(
            {"message" : "OTP code sent successfully" , "otp_session_token" : session_token},
            status=status.HTTP_200_OK)



class VerifyOtpRegisterView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = VerifyOtpSerializer

    def post(self , request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_code = serializer.validated_data['otp_code']
        session_token = serializer.validated_data['otp_session_token']

        phone_number = cache.get(otp_session_key(session_token))

        # session validation
        if not phone_number:
            return Response({"message" : "Session Expired"}, status=status.HTTP_400_BAD_REQUEST)

        attempts_key = f"otp_attempts:{phone_number}"
        attempts = cache.get(attempts_key, 0)

        if attempts >= MAX_OTP_ATTEMPTS:
            # delete data after 5 attempts
            cache.delete(otp_data_key(phone_number))
            cache.delete(otp_session_key(session_token))
            cache.delete(attempts_key)
            return Response(
                {"message": "Too many incorrect attempts. Please request a new OTP."},
                status=status.HTTP_400_BAD_REQUEST
            )

        stored_code = cache.get(otp_data_key(phone_number))

        if not stored_code:
            return Response({"message" : "Otp code Expired"}, status=status.HTTP_400_BAD_REQUEST)

        if stored_code != user_code:
            cache.set(attempts_key, attempts + 1, timeout=OTP_TTL_SECONDS)
            return Response({"message" : "OTP in incorrect"}, status=status.HTTP_400_BAD_REQUEST)

        # delete datas after successful operation
        cache.delete(otp_data_key(phone_number))
        cache.delete(otp_session_key(session_token))
        cache.delete(attempts_key)

        # generate token for complete registration
        new_session_token = generate_session_token()
        cache.set(otp_session_key(new_session_token), phone_number, timeout=600)

        return Response({
            "is_registered": False,
            "registration_token": new_session_token,
            "detail": "please complete your info"
        })


class CompleteRegisterView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = CompleteRegistrationSerializer

    def post(self , request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        token = serializer.validated_data['registration_token']

        phone_number = cache.get(otp_session_key(token))

        # token validation
        if not phone_number:
            return Response({"message" : "registration Failed"}, status=status.HTTP_400_BAD_REQUEST)

        # try for creating user and error handel when two attempts happen with same email or phone_number same time
        try:
            user = User.objects.create(
                phone_number=phone_number,
                email=serializer.validated_data['email'],
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                role=serializer.validated_data['role'],
            )
            user.set_password(serializer.validated_data['password'])
            user.save()
        except IntegrityError:
            return Response(
                {"message": "A user with this phone number or email already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # delete token in redis cache
        cache.delete(otp_session_key(token))

        #create final jwt token
        refresh = RefreshToken.for_user(user)

        return Response({
            "detail": "Registration successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_201_CREATED)




class SendOtpLoginView(APIView):
    """
    Send Otp with phone_number and save code in redis for login
    """
    authentication_classes = []
    permission_classes = []
    serializer_class = SendOtpSerializer

    def post(self , request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        phone_number = serializer.validated_data['phone_number']

        # checking for existence of phone_number
        if not User.objects.filter(phone_number=phone_number).exists():
            return Response({'message':'Phone number not found'}, status=status.HTTP_400_BAD_REQUEST)

        # check limit of sending otp in exact time
        if cache.get(otp_limit_key(phone_number)):
            return Response({"message" : "Try agin later"} , status=status.HTTP_429_TOO_MANY_REQUESTS)

        code = generate_otp_code()
        session_token = generate_session_token()

        # send OTP
        try:
            send_otp_code(phone_number, code)
        except Exception as e:
            return Response({"message" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # save datas in redis cache
        cache.set(otp_data_key(phone_number), code , timeout=OTP_TTL_SECONDS)
        cache.set(otp_limit_key(phone_number), True , timeout=OTP_RATE_LIMIT_SECONDS)
        cache.set(otp_session_key(session_token), phone_number , timeout=OTP_TTL_SECONDS)

        # delete all attempts for this phone_number
        cache.delete(f"otp_attempts:{phone_number}")

        return Response(
            {"message" : "OTP code sent successfully" , "otp_session_token" : session_token},
            status=status.HTTP_200_OK)



class VerifyOtpLoginView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = VerifyOtpSerializer

    def post(self , request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_code = serializer.validated_data['otp_code']
        session_token = serializer.validated_data['otp_session_token']

        phone_number = cache.get(otp_session_key(session_token))

        # check expiration of token
        if not phone_number:
            return Response({'message':'session expired'}, status=status.HTTP_400_BAD_REQUEST)

        attempts_key = f"otp_attempts:{phone_number}"
        attempts = cache.get(attempts_key, 0)

        if attempts >= MAX_OTP_ATTEMPTS:
            cache.delete(otp_data_key(phone_number))
            cache.delete(otp_session_key(session_token))
            cache.delete(attempts_key)
            return Response(
                        {"message": "Too many incorrect attempts. Please request a new OTP."},
                        status=status.HTTP_400_BAD_REQUEST
                )

        stored_code = cache.get(otp_data_key(phone_number))

        if not stored_code:
            return Response({'message':'Otp code expired'}, status=status.HTTP_400_BAD_REQUEST)

        if stored_code != user_code:
            cache.set(attempts_key, attempts + 1, timeout=OTP_TTL_SECONDS)
            return Response({"message" : "Code is wrong."}, status=status.HTTP_400_BAD_REQUEST)


        #delete all data in redis after successfully operation
        cache.delete(otp_data_key(phone_number))
        cache.delete(otp_session_key(session_token))
        cache.delete(attempts_key)

        try:
            user = User.objects.get(phone_number=phone_number)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)

        return Response({
            "detail": "Login successful",
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }, status=status.HTTP_200_OK)
