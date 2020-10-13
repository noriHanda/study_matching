from django.db import models
from account.models import User
from django.utils import timezone


class Notice(models.Model):
    recieved_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    body = models.CharField(max_length=8192)
    image_url = models.URLField()
    link = models.CharField(max_length=1024, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)


class UnreadNoticeCount(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (("user", ),)

    def increment(self):
        self.count += 1
        self.save()

    def reset(self):
        self.count = 0
        self.save()


