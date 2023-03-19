from django.contrib import admin
from django.urls import path,include
from .views import *
from rest_framework import routers

urlpatterns = [
    path('login/',Login,name='login'),
    path('register/',create_account,name='register'),
]
