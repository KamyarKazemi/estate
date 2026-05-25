from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self , phone_number , email , first_name , last_name , password=None , **extra_fields):
        if not phone_number:
            raise ValueError("Users must have a valid phone number")
        if not email:
            raise ValueError("Users must have a valid email")
        if not first_name:
            raise ValueError("Users must have a first name")
        if not last_name:
            raise ValueError("Users must have a last name")

        extra_fields.setdefault('role', 'CUSTOMER')

        user = self.model(
            phone_number = phone_number,
            email = self.normalize_email(email),
            first_name = first_name,
            last_name = last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self , phone_number , email , first_name , last_name , password=None ,  **extra_fields):
        extra_fields.setdefault("is_staff", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        extra_fields.setdefault("role", "ADMIN")

        if extra_fields.get("role") != "ADMIN":
            raise ValueError("Superuser must have role='ADMIN'.")

        extra_fields.setdefault("is_active", True)

        return self.create_user(phone_number , email , first_name , last_name , password , **extra_fields)