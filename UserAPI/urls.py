from django.urls import path
from . import views

urlpatterns = [
    path('generate_otp/<str:purpose>/', views.send_otp, name='send_otp'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('forgot_password/', views.forget_password, name='forgot_password'),
    path('verify_token/', views.verify_token, name='verify_token')
]
