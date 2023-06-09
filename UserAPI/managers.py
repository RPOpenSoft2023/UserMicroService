from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

class UserManager(BaseUserManager):
    def create_user(self,phone_number,password, **extra_fields):

        if not phone_number:
            raise ValueError(_("Phone must be set"))
        self.phone_number = phone_number
        user = self.model(phone_number=phone_number, **extra_fields)
        user.set_password(password)
        extra_fields.setdefault("is_active", True)

        user.save()
        return user
    def create_superuser(self,phone_number,password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        return self.create_user(phone_number, password, **extra_fields)