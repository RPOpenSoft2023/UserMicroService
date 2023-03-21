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
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def save(self, **kwargs):
        validated_data = {**self.validated_data, **kwargs}
        phone = validated_data.get('phone')
        aadhar_no = validated_data.get('aadhar_no')
        if (len(str(phone)) < 10):
            raise serializers.ValidationError("Invalid phone no.")
        if (len(str(aadhar_no)) != 12):
            raise serializers.ValidationError("Invalid aadhar no.")
        self.validated_data = validated_data
        return super().save()
