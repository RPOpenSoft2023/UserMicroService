from rest_framework import serializers
from . import models


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.User
        exclude = [
            "password","is_staff","is_active","is_superuser", "groups","user_permissions",
        ]
