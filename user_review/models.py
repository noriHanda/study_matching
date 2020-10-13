from django.db import models
from account.models import User
from django.core.validators import MaxValueValidator, MinValueValidator


class UserReview(models.Model):
    reviewer = models.ForeignKey(User, related_name='user_reviewer', on_delete=models.SET_NULL, null=True)
    reviewee = models.ForeignKey(User, related_name='user_reviewee', on_delete=models.CASCADE)
    text = models.TextField(max_length=1024)
    rating = models.PositiveIntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

