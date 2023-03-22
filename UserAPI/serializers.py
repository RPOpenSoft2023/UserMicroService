from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        exclude = [
            'password',
        ]
        read_only_fields = [
            'created_at',
            'is_staff',
            'is_superuser',
            'is_admin',
        ]
