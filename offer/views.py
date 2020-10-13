from rest_framework import viewsets

from .models import Offer
from .serializers import OfferSerializer
from rest_framework.parsers import MultiPartParser, JSONParser

from account.models import User
from account.serializers import RestrictedUserSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from user_block.models import UserBlock
from django.db.models import Count


class OfferViewSet(viewsets.ModelViewSet):
    parser_classes = (MultiPartParser, JSONParser)
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        blockList = UserBlock.objects.filter(blocking_user=request.user)
        unblock_user_offers = Offer.objects.exclude(offerer__in=list(map(lambda x: x.blocked_user, blockList)))
        return Response(OfferSerializer(unblock_user_offers, many=True).data)

    def create(self, request, *args, **kwargs):
        title = request.data.get('title')
        description = request.data.get('description')
        matching_way = request.data.get('matching_way')
        if title is not None and description is not None and matching_way is not None and request.data.get('file') is not None:
            offer = Offer.objects.create(title=title, description=description, matching_way=matching_way, offerer=request.user, image=request.data.get('file'))
            if offer is not None:
                return Response(OfferSerializer(offer).data, status=201)
        return Response({'message': '作成に失敗しました'}, status=400)

    def update(self, request, pk=None, *args, **kwargs):
        title = request.data.get('title')
        description = request.data.get('description')
        matching_way = request.data.get('matching_way')
        print(title, description, matching_way)
        existed_offer = get_object_or_404(Offer, pk=pk)
        if request.user.id != existed_offer.offerer.id:
            return Response(status=400, data={'認証エラー': '権限がありません。ログインしているユーザと別のユーザのデータを変更することはできません。'})
        if request.data.get('file') is not None:
            user_serializer = OfferSerializer(existed_offer,
                                              data={'title': title, 'description': description, 'matching_way': matching_way, 'image': request.data['file']}, partial=True)
        else:
            user_serializer = OfferSerializer(existed_offer,
                                              data={'title': title, 'description': description, 'matching_way': matching_way},
                                              partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data)
        else:
            print(user_serializer.errors)
            return Response(status=400)

    def destroy(self, request, pk=None, *args, **kwargs):
        existed_offer = get_object_or_404(Offer, pk=pk)
        if request.user.id == existed_offer.offerer.id:
            return super().destroy(request, *args, **kwargs)
        else:
            return Response(status=400, data={'認証エラー': '権限がありません。ログインしているユーザと別のユーザのデータを変更することはできません。'})


"""
    def create(self, request, *args, **kwargs):
        title = json.loads(request.body).get('title')
        description = json.loads(request.body).get('description')
        offerer = request.user
        offer = Offer.objects.create(title=title, description=description, offerer=offerer)
        if offer is not None:
            return Response(OfferSerializer(offer).data, status=201)
        else:
            return Response({'message': '作成に失敗しました'}, status=400)
"""


@permission_classes([IsAuthenticated])
@api_view(['GET'])
def fetch_user_offer_set_list(request):
    offset = int(request.GET.get('offset'))
    limit = int(request.GET.get('limit'))
    temporary_limit_extent = 100  # because client proper limit is not decided

    blockList = UserBlock.objects.filter(blocking_user=request.user)
    unblocked_users = User.objects.exclude(id__in=list(map(lambda x: x.blocked_user.id, blockList))).order_by('-id')

    sortedUserOfferSetList=fetch_users_and_offers(unblocked_users, offset, limit, temporary_limit_extent)
    return Response(status=200, data=sortedUserOfferSetList)


@api_view(['GET'])
def fetch_user_offer_set_list_logged_out(request):
    offset = int(request.GET.get('offset'))
    limit = int(request.GET.get('limit'))
    users = User.objects.all().order_by('-id')
    temporary_limit_extent = 100  # because client proper limit is not decided

    sortedUserOfferSetListLoggedOut=fetch_users_and_offers(users, offset, limit, temporary_limit_extent)
    return Response(status=200, data=sortedUserOfferSetListLoggedOut)


def fetch_users_and_offers(users, offset, limit, temporary_limit_extent):
    userOfferSetList = []
    for user in users.annotate(num_offers=Count('offers')).filter(num_offers__gte=1):
        userOfferSet = {}
        restrictedUserSerializer = RestrictedUserSerializer(user)
        userOfferSet['user'] = restrictedUserSerializer.data
        offerListSerializer = OfferSerializer(Offer.objects.filter(offerer=user).order_by('-created_at')[0:3],
                                              many=True)
        userOfferSet['offers'] = offerListSerializer.data
        if len(userOfferSet['offers']) != 0:
            userOfferSetList.append(userOfferSet)
    return sorted(userOfferSetList, key=lambda x: x['offers'][0]['created_at'], reverse=True)[
                             offset:offset + limit + temporary_limit_extent]


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_individual_user_offer_list(request):
    user_id = int(request.GET.get('userId'))
    blockList = UserBlock.objects.filter(blocking_user=request.user)
    if user_id in list(map(lambda x: x.blocked_user.id, blockList)):
        offer_list_serializer = OfferSerializer([], many=True)
    else:
        offer_list_serializer = OfferSerializer(Offer.objects.filter(offerer_id=user_id).order_by('-updated_at'),
                                                many=True)
    return Response(offer_list_serializer.data)
