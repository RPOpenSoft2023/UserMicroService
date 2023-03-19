
from rest_framework import viewsets
from .serializers import UserSerializer
from rest_framework.response import Response

from . import models

# create a viewset
class UsersViewSet(viewsets.ModelViewSet):
    queryset = models.User.objects.all()
    serializer_class = UserSerializer
