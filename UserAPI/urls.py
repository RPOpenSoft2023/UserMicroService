from django.urls import path
from .views import *

urlpatterns = [
    path('send_otp/', send_otp , name="send_otp"),
]
