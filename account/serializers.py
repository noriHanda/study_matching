from rest_framework import serializers
from versatileimagefield.serializers import VersatileImageFieldSerializer

from .models import User


class MyUserSerializer(serializers.ModelSerializer):
    icon = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail_url', 'thumbnail__300x300'),
        ]
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'intro', 'faculty', 'department', 'grade', 'hobby', 'want_to_know', 'want_to_teach', 'icon', 'date_joined', 'is_active', 'user_tags')


class RestrictedUserSerializer(serializers.ModelSerializer):
    icon = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail_url', 'thumbnail__300x300'),
        ]
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'intro', 'faculty', 'department', 'grade', 'hobby', 'want_to_know', 'want_to_teach', 'icon', 'user_tags')
