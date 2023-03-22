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
from django.contrib.auth import get_user_model


# Create your views here.
@api_view(['POST'])
def login(request):
    try:
        ph_No = request.data["phone_number"]
        password = request.data["password"]
        
        user = authenticate(phone=int(ph_No), password=password)
        
        if (user is None):
            return Response({'error': 'Credentials invalid'}, status=401)
        jwt_token = jwt.encode(
            {
                'phone':
                ph_No,
                'exp':
                datetime.datetime.now() +
                datetime.timedelta(settings.JWT_EXPIRY_TIME)
            },
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM)
        return Response(
            {
                'jwt_token': jwt_token,
                'message': 'Logged In Successfully'
            },
            status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=401)


# generate otp function here
@api_view(['POST'])
def send_otp(request):
    try:
        ph = request.data['phone_number']

        account_sid = settings.ACCOUNTS_SID
        auth_token = settings.AUTH_TOKEN
        client = Client(account_sid, auth_token)
        otp = random.randint(100000, 999999)
        message = client.messages.create(body="Hello from ShiftBank, Your OTP is " +
                                         str(otp),
                                         from_=settings.PHONE,
                                         to='+91' + ph)
        
        new_token = jwt.encode(
            {
                'phone':
                ph,
                'otp':
                otp,
                'exp':
                datetime.datetime.now() +
                datetime.timedelta(settings.JWT_EXPIRY_TIME)
            },
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM)
        return Response({
            'message': 'OTP sent',
            'jwt_token': new_token
        },
                        status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=401)


#verify otp function here
@api_view(['POST'])
def verify_otp(request):
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'Authorization header is missing'},
                            status=status.HTTP_401_UNAUTHORIZED)
        _, token = auth_header.split()
        decoded_token = jwt.decode(token,
                                   settings.JWT_SECRET,
                                   algorithms=[settings.JWT_ALGORITHM])
        actual_otp = decoded_token.get('otp')
        phone_number = decoded_token.get('phone')

        user_otp = request.data.get('otp')
        if not user_otp:
            return Response({'error': 'User OTP is missing'},
                            status=status.HTTP_400_BAD_REQUEST)

        if user_otp != actual_otp:
            return Response({'error': 'Invalid OTP'},
                            status=status.HTTP_401_UNAUTHORIZED)

        new_token = jwt.encode(
            {
                'phone':
                phone_number,
                'exp':
                datetime.datetime.now() +
                datetime.timedelta(settings.JWT_EXPIRY_TIME)
            },
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM)

        return Response({'token': new_token}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def register(request):
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'Authorization header is missing'},
                            status=status.HTTP_401_UNAUTHORIZED)
        _, token = auth_header.split()
        decoded_token = jwt.decode(token,
                                   settings.JWT_SECRET,
                                   algorithms=[settings.JWT_ALGORITHM])
        user = models.User.objects.get(decoded_token.get('phone'))
        if (user is not None):
            return Response(
                {
                    'message':
                    'an account with that phone number already exists'
                },
                status=400)
        user = serializers.UserSerializer(data=request.data)
        user.is_valid(raise_exception=True)
        user.save()
        return Response({'message': 'account created successfully'})
    except Exception as e:
        return Response({'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def forget_password(request):
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'Authorization header is missing'},
                            status=status.HTTP_401_UNAUTHORIZED)
        _, token = auth_header.split()
        decoded_token = jwt.decode(token,
                                   settings.JWT_SECRET,
                                   algorithms=settings.JWT_ALGORITHM)
        actual_otp = decoded_token.get('otp')
        phone_number = decoded_token.get('phone')
        user_otp = request.data.get('otp')
        new_password = request.data.get('new_password')

        if not user_otp or not new_password:
            return Response({'error': 'User OTP or new password is missing'},
                            status=status.HTTP_400_BAD_REQUEST)

        if user_otp != actual_otp:
            return Response({'error': 'Invalid OTP'},
                            status=status.HTTP_401_UNAUTHORIZED)

        User = get_user_model()
        try:
            user = User.objects.get(phone_number=phone_number)
            user.set_password(new_password)
            user.save()
        except User.DoesNotExist:
            return Response({'error': 'User not found'},
                            status=status.HTTP_404_NOT_FOUND)

        return Response({'message': "Password changed successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
def verify_token(request):
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'error': 'Authorization header is missing'},
                            status=status.HTTP_401_UNAUTHORIZED)
        _, token = auth_header.split()
        decoded_token = jwt.decode(token,
                                   settings.JWT_SECRET,
                                   algorithms=settings.JWT_ALGORITHM)
        phone_number = decoded_token.get('phone')
        user = serializers.UserSerializer(
            models.User.objects.get(pk=phone_number))
        return Response(user.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
