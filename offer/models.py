from django.db import models
from django.conf import settings
from versatileimagefield.fields import VersatileImageField


class Offer(models.Model):
    offerer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='offers')
    title = models.CharField(max_length=128)
    description = models.TextField()
    matching_way = models.CharField(default='チャットメインで！', max_length=32)
    image = VersatileImageField('',upload_to='offer', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

