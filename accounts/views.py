from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SendOtpSerializer, VerifyOtpSerializer, CompleteRegistrationSerializer
from .otp import *
from .utils import send_otp_code
from django.core.cache import cache
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from .services.otp_service import OTPService


User = get_user_model()




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

        # send OTP
        try:
            session_token = OTPService.send_otp(phone_number)
        except Exception as e:
            return Response({"message" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            {"message" : "OTP code sent successfully" , "otp_session_token" : session_token}
            ,status=status.HTTP_200_OK)


class VerifyOtpRegisterView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = VerifyOtpSerializer

    def post(self , request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            phone_number = OTPService.verify_otp(
                serializer.validated_data['otp_session_token'],
                serializer.validated_data['otp_code'],
            )
        except Exception as e:
            return Response({"message" : str(e)}, status=status.HTTP_400_BAD_REQUEST)

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

        # send OTP
        try:
            session_token = OTPService.send_otp(phone_number)
        except Exception as e:
            return Response({"message" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            {"message" : "OTP code sent successfully" , "otp_session_token" : session_token}
            ,status=status.HTTP_200_OK)


class VerifyOtpLoginView(APIView):
    authentication_classes = []
    permission_classes = []
    serializer_class = VerifyOtpSerializer

    def post(self , request):
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)

        try:
            phone_number = OTPService.verify_otp(
                serializer.validated_data['otp_session_token'],
                serializer.validated_data['otp_code'],
            )
        except Exception as e:
            return Response({"message" : str(e)}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(phone_number=phone_number).first()

        refresh = RefreshToken.for_user(user)

        return Response({
            "access" : str(refresh.access_token),
            "refresh" : str(refresh)
        })


