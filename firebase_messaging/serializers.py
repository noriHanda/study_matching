from rest_framework import serializers
from .models import FCMDeviceToken


class FCMDeviseTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDeviceToken
        fields = ('device_token',)
