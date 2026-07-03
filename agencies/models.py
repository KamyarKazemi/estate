from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Agency(models.Model):
    agent = models.OneToOneField(User , on_delete=models.CASCADE , related_name='agency')
    name = models.CharField(max_length=255)
    license_number = models.CharField(max_length=155)
    business_phone = models.CharField(max_length=11)
    description = models.TextField()
    province = models.CharField(max_length=122)
    city = models.CharField(max_length=122)
    exact_address = models.TextField()
    is_verified = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "agency"
        verbose_name_plural = "agencies"



