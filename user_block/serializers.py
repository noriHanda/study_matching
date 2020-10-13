from rest_framework import serializers
from .models import UserBlock


class UserBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBlock
        fields = ('id', 'blocked_user', 'blocking_user', 'created_at')
        
