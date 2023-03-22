from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display=('phone_number','email')

admin.site.register(User, UserAdmin)
admin.site.register(OTPModel)
