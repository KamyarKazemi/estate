from rest_framework import serializers
from agencies.models import Agency
from rest_framework.serializers import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class AgencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ('name' , 'license_number' , 'business_phone' , 'description' , 'province' , 'city' , 'exact_address')





