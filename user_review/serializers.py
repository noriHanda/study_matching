from rest_framework import serializers

from .models import UserReview


class UserReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserReview
        fields = ('id', 'reviewer', 'reviewee', 'text', 'rating', 'created_at')
