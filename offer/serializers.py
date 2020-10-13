from rest_framework import serializers

from .models import Offer
from versatileimagefield.serializers import VersatileImageFieldSerializer


class OfferSerializer(serializers.ModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes=[
            ('full_size', 'url'),
            ('thumbnail_url', 'thumbnail__300x300'),
        ]
    )

    class Meta:
        model = Offer
        fields = ('id', 'offerer', 'title', 'description', 'matching_way', 'image', 'created_at',)
