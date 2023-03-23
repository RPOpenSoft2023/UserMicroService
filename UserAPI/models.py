from django.db import models
from django.contrib.auth.models import (PermissionsMixin, BaseUserManager,
                                        AbstractBaseUser)
from django.utils import timezone
from .managers import UserManager
import datetime
from django.conf import settings

# Create your models here.
class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=10, unique=True, primary_key=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    aadhar_no = models.CharField(max_length=12, null=True, blank=True, unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    reports_count = models.IntegerField(null=True, blank=True)
    accounts_count = models.IntegerField(null=True, blank=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    REQUIRED_FIELDS = ['aadhar_no', 'email']
    USERNAME_FIELD = 'phone_number'
    objects = UserManager()

    def __str__(self):
        return str(self.phone_number)
    
class OTPModel(models.Model):
    PURPOSE_CHOICES = (
        ('verify_phone_number','verify_phone_number'),
        ('reset_password','reset_password')
    )
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    valid_until = models.DateTimeField(help_text="The timestamp of the moment of expiry of the saved token.")
    purpose = models.CharField(max_length=255, null=True, blank=True, choices=PURPOSE_CHOICES)

    def __str__(self):
        return str(self.phone_number)