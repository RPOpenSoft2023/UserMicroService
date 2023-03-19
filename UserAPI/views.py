import os
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from twilio.rest import Client
# from .helpers import send_otp_to_phone 
from .models import User
from django.conf import settings
import random
import jwt
import datetime

# Create your views here.
@api_view(['POST'])
def send_otp(request):
    try:
        data = request.data
        ph = data.get('phone_number')
        print(ph)
        account_sid = settings.ACCOUNTS_SID
        # auth_token = os.environ["TWILIO_AUTH_TOKEN"]
        auth_token = settings.AUTH_TOKEN
        client = Client(account_sid, auth_token)
        otp = random.randint(100000,999999)
        message = client.messages.create(
        body="Hello from Harsh, OTP is " + str(otp),
        from_=settings.PHONE,
        to='+91'+ph
        )
        print(message.sid)
        new_token = jwt.encode({'phone_number': ph, 'otp':otp, 'exp':datetime.datetime.now()+datetime.timedelta(settings.JWT_EXPIRY_TIME)}, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return Response({
            'message':'OTP sent',
            'jwt_token': new_token
        }, status=200)
    except Exception as e:
        return Response({"error":str(e)}, status=401)