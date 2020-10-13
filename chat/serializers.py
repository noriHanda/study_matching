from rest_framework import serializers

from .models import Chat, Talk, ChatUnreadTalkCount


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = ('id', 'user1', 'user2', 'created_at')


class TalkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Talk
        fields = ('id', 'talker', 'chat', 'sentence', 'created_at')


class ChatUnreadTalkCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatUnreadTalkCount
        fields = ('id', 'chat', 'count', 'user')
