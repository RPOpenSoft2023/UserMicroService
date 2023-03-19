from django.db import models
from django.contrib.auth.models import (PermissionsMixin,BaseUserManager, AbstractBaseUser )
from django.utils import timezone
from .managers import UserManager
from .import constants as user_constants
from django.core.validators import RegexValidator

# Create your models here.

class User(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    phone = models.BigIntegerField(unique = True)
    email = models.EmailField(unique=True, null=True, db_index=True)
    aadhar_no = models.BigIntegerField(null=True, blank=True, unique=True)
    date_of_birth = models.DateField(null = True, blank=True)
    age = models.IntegerField(null = True,blank=True)
    gender = models.CharField(max_length= 255,null=True, blank = True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    city = models.CharField(max_length=255,null = True,blank=True)
    state = models.CharField(max_length=255, null = True, blank=True)

    REQUIRED_FIELDS = ['aadhar_no','email']
    USERNAME_FIELD = 'phone'

    objects = UserManager()

    def __str__(self):
        return str(self.phone)
