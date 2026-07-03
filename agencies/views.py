from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import AgencyCreateSerializer


class CreateAgencyView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AgencyCreateSerializer

    def post(self , request):
        serializer = self.serializer_class(data=request.data , context={'request':request})
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(serializer.data , status=status.HTTP_201_CREATED)