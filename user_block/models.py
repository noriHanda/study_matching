from django.db import models
from account.models import User


class UserBlock(models.Model):
    blocked_user = models.ForeignKey(User, related_name='user_blocked', on_delete=models.SET_NULL, null=True)
    blocking_user = models.ForeignKey(User, related_name='user_blocking', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

