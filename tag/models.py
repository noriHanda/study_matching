from django.db import models
from account.models import User


class Tag(models.Model):
    users = models.ManyToManyField(User, related_name='user_tags')
    name = models.CharField(max_length=32)
    category = models.CharField(max_length=32, default='university')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
