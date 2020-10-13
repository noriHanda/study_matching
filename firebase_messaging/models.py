from django.db import models
from account.models import User
from django.utils import timezone


class FCMDeviceToken(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    device_token = models.TextField(blank=False, null=False, unique=True)
    created_date = models.DateTimeField(default=timezone.now)

