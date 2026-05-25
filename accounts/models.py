from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        AGENT = 'AGENT', 'بنگاه‌دار'
        CUSTOMER = 'CUSTOMER', 'مشتری'
        ADMIN = 'ADMIN', 'مدیر'

    phone_number = models.CharField(max_length=11, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=22, choices=Role.choices, default=Role.CUSTOMER)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email' , 'first_name' , 'last_name']

    def __str__(self):
        return f"{self.phone_number} - {self.first_name} {self.last_name}"