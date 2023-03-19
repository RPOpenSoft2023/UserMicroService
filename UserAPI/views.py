import jwt
import datetime
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework import viewsets

from . import models, serializers

# create a viewset
class UsersViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer

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
