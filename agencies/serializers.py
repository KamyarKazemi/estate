from rest_framework import serializers
from agencies.models import Agency
from rest_framework.serializers import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()


class AgencyCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agency
        fields = ('name' , 'license_number' , 'business_phone' , 'description' , 'province' , 'city' , 'exact_address')

    def validate(self, data):
        user = self.context['request'].user
        if user.role != User.Role.AGENT:
            raise ValidationError("Only AGENT can create agencies")
        return data

    def create(self, validated_data):
        agency = Agency.objects.create(
            agent = self.context['request'].user,
            **validated_data
        )

        return agency



