from django.db import models
from django.utils import timezone
from django.conf import settings
from offer.models import Offer
from account.models import User


class Chat(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='chat_user1', null=True)
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='chat_user2', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Talk(models.Model):
    talker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sentence = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class ChatUnreadTalkCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    count = models.PositiveIntegerField(default=0)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("user", "chat"),)

    def increment(self):
        self.count += 1
        self.save()

    def reset(self):
        self.count = 0
        self.save()
