from rest_framework.decorators import api_view
from rest_framework.response import Response
from twilio.rest import Client
from django.conf import settings
import random
import jwt
import datetime
from django.contrib.auth import authenticate
from rest_framework import status
from .models import *
from .serializers import *
from django.contrib.auth import get_user_model


# Create your views here.
@api_view(['POST'])
def login(request):
    try:
        phone_number = request.data["phone_number"]
        password = request.data["password"]
        
        user = authenticate(phone_number=str(phone_number), password=password)
        
        if (user is None):
            return Response({'error': 'Credentials invalid'}, status=401)
        jwt_token = jwt.encode(
            {
                'phone_number':phone_number,
                'exp': timezone.now() + datetime.timedelta(settings.JWT_EXPIRY_TIME),
                'iat': timezone.now()
            },
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM)
        return Response({
            'message': 'Logged In Successfully',
            'login_token': jwt_token
            }, status=200)
    except Exception as e:
        return Response({'error': str(e)}, status=401)


# generate otp function here
@api_view(['POST'])
def send_otp(request, purpose):
    try:
        phone_number = request.data['phone_number']

        account_sid = settings.ACCOUNTS_SID
        auth_token = settings.AUTH_TOKEN
        client = Client(account_sid, auth_token)
        otp = random.randint(100000, 999999)
        message = client.messages.create(body="Hello from ShiftBank, Your OTP is " +
                                         str(otp),
                                         from_=settings.PHONE,
                                         to='+91' + phone_number)
        otp_obj = OTPModel.objects.filter(phone_number=phone_number).filter(purpose=purpose).first()
        if otp_obj is not None:
            otp_obj.delete()
        print(purpose)
        otp_obj = OTPModel.objects.create(otp=otp, phone_number=phone_number, purpose=purpose,valid_until=timezone.now()+datetime.timedelta(seconds=settings.OTP_EXPIRY_TIME))
        otp_obj.save()

        return Response({'message': 'OTP sent'}, status=200)
    except Exception as e:
        return Response({"error": str(e)}, status=401)


#verify otp function here
@api_view(['POST'])
def verify_otp(request):
    try:

        phone_number = request.data["phone_number"]
        user_otp = request.data.get('otp')

        otp_obj = OTPModel.objects.filter(phone_number=phone_number).first()
        print(otp_obj.otp)
        if otp_obj is None:
            return Response({"error":"No OTP is sent on this phone number"}, status=400)

        if not user_otp:
            return Response({'error': 'User OTP is missing'}, status=status.HTTP_400_BAD_REQUEST)

        if str(user_otp) != str(otp_obj.otp):
            return Response({'error': 'Invalid OTP'},
                            status=status.HTTP_401_UNAUTHORIZED)
        
        if otp_obj.valid_until < timezone.now():
            return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        otp_obj.delete()

        new_token = jwt.encode({
            'phone_number': phone_number,
            'exp': timezone.now() + datetime.timedelta(settings.JWT_EXPIRY_TIME),
            'iat': timezone.now()
            },
            settings.JWT_SECRET,
            algorithm=settings.JWT_ALGORITHM)

        return Response({'register_token': new_token}, status=status.HTTP_200_OK)
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
        
        phone_number = decoded_token.get('phone_number')

        user = User.objects.filter(phone_number=phone_number).first()
        
        if user is not None:
            return Response({'error':'An account with this phone number already exists'}, status=400)
        
        if "password" not in request.data:
            return Response({"error":"Password not present"}, status=400)
        
        if request.data["password"] == "":
            return Response({"error":"Don't send password as empty"}, status=400)
        
        if "aadhar_no" not in request.data:
            return Response({"error":"Aadhar number not present"}, status=400)
        
        aadhar_no = request.data['aadhar_no']
        if len(str(aadhar_no)) != 12:
            return Response({'error':'Invalid Aadhar number'}, status=400)
        
        data = {}

        for key in request.data:
            print(key)
            if "phone_number" == key or "password" == key: continue
            data[key] = request.data[key]

        data["phone_number"] = phone_number

        try:
            user = User(**data)
            user.set_password(request.data["password"])
            user.save()
        except Exception as e:
            return Response({"error":str(e)}, status=400)
        return Response({'message': 'Account created successfully'})
    except Exception as e:
        return Response({'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
def forget_password(request):
    try:
        phone_number = request.data.get('phone_number')
        user_otp = request.data.get('otp')
        new_password = request.data.get('new_password')

        otp_obj = OTPModel.objects.filter(phone_number=phone_number).first()
        
        if otp_obj is None:
            return Response({"error":"No OTP is sent on this phone number"}, status=400)

        if not user_otp:
            return Response({'error': 'User OTP is missing'}, status=status.HTTP_400_BAD_REQUEST)

        if str(user_otp) != str(otp_obj.otp):
            return Response({'error': 'Invalid OTP'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if otp_obj.valid_until < timezone.now():
            return Response({'error': 'OTP has expired'}, status=status.HTTP_400_BAD_REQUEST)
        
        if new_password is None:
            return Response({'error': 'New password is missing'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(phone_number=phone_number)
            user.set_password(new_password)
            user.save()
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'message': "Password changed successfully"}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
        phone_number = decoded_token.get('phone_number')
        user = User.objects.filter(phone_number=phone_number).first()
        if user is None:
            return Response({"error":"No user exists with this phone number"}, status=400)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
