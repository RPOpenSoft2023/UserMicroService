from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
import jwt
from django.contrib.auth import get_user_model
from django.conf import settings
import datetime

@api_view(['POST'])
def verify_otp(request):
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'message': 'Authorization header is missing'}, status=status.HTTP_401_UNAUTHORIZED)
        _, token = auth_header.split()
        # print("token: ",token)
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        actual_otp = decoded_token.get('otp')
        phone_number = decoded_token.get('phone_number')
        # print(actual_otp, phone_number)

        user_otp = request.data.get('otp')
        if not user_otp:
            return Response({'message': 'User OTP is missing'}, status=status.HTTP_400_BAD_REQUEST)

        if user_otp != actual_otp:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_401_UNAUTHORIZED)

        new_token = jwt.encode({'phone_number': phone_number, 'exp':datetime.datetime.now()+datetime.timedelta(settings.JWT_EXPIRY_TIME)}, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

        return Response({'token': new_token}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['PUT'])
def forget_password(request):
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response({'message': 'Authorization header is missing'}, status=status.HTTP_401_UNAUTHORIZED)
        _, token = auth_header.split()
        decoded_token = jwt.decode(token, settings.JWT_SECRET, algorithms=settings.JWT_ALGORITHM)
        actual_otp = decoded_token.get('otp')
        phone_number = decoded_token.get('phone_number')

        user_otp = request.data.get('otp')
        new_password = request.data.get('new_password')
        if not user_otp or not new_password:
            return Response({'message': 'User OTP or new password is missing'}, status=status.HTTP_400_BAD_REQUEST)

        if user_otp != actual_otp:
            return Response({'message': 'Invalid OTP'}, status=status.HTTP_401_UNAUTHORIZED)

        User = get_user_model()
        try:
            user = User.objects.get(phone_number=phone_number)
            user.set_password(new_password)
            user.save()
        except User.DoesNotExist:
            return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        new_token = jwt.encode({'phone_number': phone_number,'exp':datetime.datetime.now()+datetime.timedelta(settings.JWT_EXPIRY_TIME)}, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

        return Response({'token': new_token}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
