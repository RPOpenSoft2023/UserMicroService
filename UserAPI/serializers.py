from rest_framework import serializers
from . import models

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=models.User
        fields="__all__"

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = self.Meta.model(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def save(self, **kwargs):
        phone = self.validated_data.get('phone')
        if (len(str(phone))<10):
            raise serializers.ValidationError("Invalid phone no.")
        aadhar_no = self.validated_data.get('aadhar_no')
        if (len(str(aadhar_no))<12):
            raise serializers.ValidationError("Invalid aadhar no.")
        return super().save(**kwargs)
