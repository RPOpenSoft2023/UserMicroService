from django.urls import path
from .views import *

urlpatterns = [
    path('send_otp/', send_otp , name="send_otp"),
    path('login/',Login,name='login'),
    path('register/',create_account,name='register'),
]
