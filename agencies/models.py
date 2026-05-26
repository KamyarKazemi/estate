from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Agency(models.Model):
    """agent"""
    agent = models.OneToOneField(User , on_delete=models.CASCADE , related_name='agency')
    """agency Information"""
    name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=155)
    business_phone = models.CharField(max_length=11)
    description = models.TextField()
    """verify"""
    is_verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "agency"
        verbose_name_plural = "agencies"


class AgencyAddress(models.Model):
    """agency"""
    agency = models.OneToOneField(Agency , on_delete=models.CASCADE , related_name='address')
    """address Information step by step"""
    province = models.CharField(max_length=122)
    city = models.CharField(max_length=122)
    exact_address = models.TextField()

    class Meta:
        verbose_name = "agency_address"
        verbose_name_plural = "agency_addresses"
