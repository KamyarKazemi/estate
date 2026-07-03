from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import AgencySerializer
from .permissions import IsAgent


class CreateAgencyView(APIView):
    """
    create agency just for authenticated agent
    """
    permission_classes = [IsAgent]
    serializer_class = AgencySerializer

    def post(self , request):
        if Agency.objects.filter(agent = request.user).exists():
            return Response({"message" : "you already have an agency"} , status = status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data , context={'request':request})
        serializer.is_valid(raise_exception=True)

        serializer.save(agent = request.user)
        return Response(serializer.data , status=status.HTTP_201_CREATED)


class UpdateAgencyView(APIView):
    """
    update agency just for authenticated agent
    """
    permission_classes = [IsAgent]
    serializer_class = AgencySerializer

    def patch(self , request):
        try:
            agency = request.user.agency
        except Agency.DoesNotExist:
            return Response({"message":"Agency not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance=agency ,
                                           data = request.data ,
                                           partial=True,
                                           context={'request':request} ,)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data , status=status.HTTP_200_OK)