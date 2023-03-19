from django.urls import path
from .views import *

urlpatterns = [
    path('verify_otp/', verify_otp),
    path('forget_password/', forget_password)
]