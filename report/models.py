from django.db import models
from account.models import User


class Report(models.Model):
    reporting_user = models.ForeignKey(User, related_name='user_reporting', on_delete=models.CASCADE, null=True)
    reported_user = models.ForeignKey(User, related_name='user_reported', on_delete=models.SET_NULL, null=True)
    content = models.CharField(max_length=512)
    created_at = models.DateTimeField(auto_now=True)
