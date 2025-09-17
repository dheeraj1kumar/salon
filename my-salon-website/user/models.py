from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from datetime import timedelta,datetime
import random
from django.utils.timezone import localtime



class CustomUserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError("Phone number is required")
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, password, **extra_fields)



class CustomUser(AbstractUser):
    username = None   
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(blank=True, null=True)
    name = models.CharField(max_length=100, blank=True, null=True,)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.phone




class OTP(models.Model):
    phone = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    EXPIRATION_MINUTES = 5 

    def __str__(self):
        return f"{self.phone} - {self.code}"

    @classmethod
    def generate_otp(cls):
        return str(random.randint(100000, 999999))

    def is_valid(self):
        now = localtime(timezone.now())
        return now <= self.created_at + timedelta(minutes=self.EXPIRATION_MINUTES)
