import os
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from twilio.rest import Client
from django.conf import settings
import random
import jwt
import datetime
from django.contrib.auth import authenticate
from rest_framework import status
from . import models, serializers


# Create your views here.
@api_view(['POST'])
def Login(request):
    try:
        print(request.data)
        ph_No = request.data["phone"]
        password = request.data["password"]
        user = authenticate(phone=ph_No, password=password)
        if (user is None):
            return Response({
                'message': 'credentials invalid'}, status=401)
        jwt_token = jwt.encode({'phone': ph_No,
            'exp': datetime.datetime.now()+datetime.timedelta(settings.JWT_EXPIRY_TIME)
            }, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)
        return Response({'jwt_token': jwt_token, 'message': 'Logged In Successfully'}, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=401)
@api_view(['POST'])


# generate otp function here
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



#verify otp function here

def create_account(request):
    
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'message': 'Authorization header is missing'}, status=status.HTTP_401_UNAUTHORIZED)
        _, token = auth_header.split()
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        user_exists = models.User.objects.get(decoded_token.get('phone'))
        if(user_exists is not None) :
            return Response({'message':'an account with that phone number already exists'},status=400)
        new_user = serializers.UserSerializer(request)
        new_user.save()
        return Response({'message':'account created successfully'})
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
