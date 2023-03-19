
from rest_framework import viewsets
from .serializers import UserapiSerializer
from rest_framework.response import Response

from .models import *

# create a viewset
class UsersViewSet(viewsets.ModelViewSet):
    
    queryset = UserAPI.objects.all()
    
    serializer_class = UserapiSerializer
    
    
   