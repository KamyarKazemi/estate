from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import SendOtpSerializer
from .otp import *
from .utils import send_otp_code
import json
from django.core.cache import cache

class SendOtpView(APIView):
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

        if cache.get(otp_limit_key(phone_number)):
            return Response({"message" : "Try agin later"} , status=status.HTTP_429_TOO_MANY_REQUESTS)

        code = generate_otp_code()

        try:
            send_otp_code(phone_number, code)
        except Exception as e:
            return Response({"message" : str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        cache.set(otp_data_key(phone_number), code , timeout=OTP_TTL_SECONDS)
        cache.set(otp_limit_key(phone_number), True , timeout=OTP_RATE_LIMIT_SECONDS)

        return Response({"message" : "OTP code sent successfully"}, status=status.HTTP_200_OK)