from tag.models import Tag
from offer.models import Offer
from account.models import User
import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from offer.serializers import OfferSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def search_offer_with_tags(request):
    tag_ids = json.loads(request.body).get('user_tags')
    users_having_query_tags = User.objects.filter(user_tags__in=tag_ids).distinct()
    result = []
    for user in users_having_query_tags:
        result += user.offers.all()

    return Response(OfferSerializer(result, many=True).data)

