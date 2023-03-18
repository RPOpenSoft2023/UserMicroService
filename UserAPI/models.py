from django.db import models
from django.contrib.auth.models import (PermissionsMixin,BaseUserManager, AbstractBaseUser )
from django.utils import timezone
from .managers import UserManager
from .import constants as user_constants
from django.core.validators import RegexValidator

# Create your models here.

class UserAPI(AbstractBaseUser, PermissionsMixin):

    first_name = models.CharField(max_length = 255)
    lastname = models.CharField(max_length = 255)
    phone = models.BigIntegerField(unique = True)
    email = models.EmailField(unique=True, null=True, db_index=True)
    aadhar_no = models.BigIntegerField(null=True, blank=True)
    age = models.IntegerField(null = True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    REQUIRED_FIELDS = ['aadhar_no','email']
    USERNAME_FIELD = 'phone'

    objects = UserManager()

    def __str__(self):
        return str(self.phone)
