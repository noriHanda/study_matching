import json
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated


from rest_framework import viewsets

from .models import Talk, Chat, ChatUnreadTalkCount
from .serializers import TalkSerializer, ChatSerializer, ChatUnreadTalkCountSerializer
from account.serializers import RestrictedUserSerializer
from .utils import notify_talk_recieve


class ChatViewSet(viewsets.ModelViewSet):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user1_id = json.loads(request.body).get('user1')
        user2_id = json.loads(request.body).get('user2')
        print(request.body)
        if user1_id != user2_id:
            if user1_id and user2_id:
                if Chat.objects.filter(
                Q(user1_id=user1_id, user2_id=user2_id) | Q(user1_id=user2_id, user2_id=user1_id)).count() == 0:
                    chat_data = ChatSerializer(Chat.objects.create(
                        user2_id=user2_id,
                        user1_id=user1_id)).data
                    if(chat_data):
                        return Response(chat_data, status=201)
        return Response(status=400)

    def list(self, request, *args, **kwargs):
        return Response(status=400, data={'認証エラー': '権限がありません。チャットルームの一覧を取得することはできません。'})

    def retrieve(self, request, pk=None, *args, **kwargs):
        existed_chat = get_object_or_404(Chat, pk=pk)
        if request.user in [existed_chat.user1, existed_chat.user2]:
            return super().retrieve(request, *args, **kwargs)
        else:
            return Response(status=400, data={'認証エラー': '権限がありません。ログインしているユーザと別のユーザのデータを取得することはできません。'})

    def update(self, request, pk=None, *args, **kwargs):
        existed_chat = get_object_or_404(Chat, pk=pk)
        if request.user in [existed_chat.user1, existed_chat.user2]:
            return super().update(request, *args, **kwargs)
        else:
            return Response(status=400, data={'認証エラー': '権限がありません。ログインしているユーザと別のユーザのデータを変更することはできません。'})

    def partial_update(self, request, pk=None, *args, **kwargs):
        existed_chat = get_object_or_404(Chat, pk=pk)
        if request.user in [existed_chat.user1, existed_chat.user2]:
            return super().partial_update(request, *args, **kwargs)
        else:
            return Response(status=400, data={'認証エラー': '権限がありません。ログインしているユーザと別のユーザのデータを変更することはできません。'})

    def destroy(self, request, pk=None, *args, **kwargs):
        return Response(status=400, data={'認証エラー': '権限がありません。チャットルームの削除はできません。'})


class TalkViewSet(viewsets.ModelViewSet):
    queryset = Talk.objects.all()
    serializer_class = TalkSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        return Response(status=400, data={'認証エラー': '権限がありません。メッセージの一覧を取得することはできません。'})

    def retrieve(self, request, pk=None, *args, **kwargs):
        return Response(status=400, data={'認証エラー': '権限がありません。APIから特定のメッセージを取得することはできません。'})

    def destroy(self, request, pk=None, *args, **kwargs):
        return Response(status=400, data={'認証エラー': '権限がありません。メッセージの削除はできません。'})

    def update(self, request, pk=None, *args, **kwargs):
        return Response(status=400, data={'認証エラー': '権限がありません。メッセージの更新はできません。'})

    def partial_update(self, request, pk=None, *args, **kwargs):
        return Response(status=400, data={'認証エラー': '権限がありません。メッセージの更新はできません。'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def search_chat(request):
    user1_id = json.loads(request.body).get('user1_id')
    user2_id = json.loads(request.body).get('user2_id')
    if request.user.id in [user1_id, user2_id]:
        return Response(ChatSerializer(Chat.objects.get(
            user2_id=user2_id,
            user1_id=user1_id)).data
        )
    else:
        return Response(status=400, data={'認証エラー': '権限がありません。ログインしているユーザと別のユーザのデータを取得することはできません。'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_my_chat(request):
    my_user_id = request.user.id
    return Response(
        ChatSerializer(
            Chat.objects.filter(
                Q(user2_id=my_user_id) | Q(user1_id=my_user_id)
            ).order_by('-updated_at'),
            many=True
        ).data
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_latest_talk(request):
    chat_id = request.GET.get('chat_id')
    existed_chat = get_object_or_404(Chat, pk=chat_id)
    if request.user in [existed_chat.user1, existed_chat.user2]:
        return Response(
            TalkSerializer(
                Talk.objects.filter(
                    chat=chat_id).order_by('-created_at')[0]
            ).data
        )
    else:
        return Response(status=400, data={'認証エラー': '権限がありません。ログインしているユーザと別のユーザのデータを取得することはできません。'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_all_talk(request):
    chat_id = request.GET.get('chat_id')
    existed_chat = get_object_or_404(Chat, pk=chat_id)
    if request.user in [existed_chat.user1, existed_chat.user2]:
        return Response(
            TalkSerializer(
                Talk.objects.filter(
                    chat=chat_id).order_by('created_at'),
        many=True)
            .data
        )
    else:
        return Response(status=400, data={'認証エラー': '権限がありません。ログインしているユーザと別のユーザのデータを取得することはできません。'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_chat_with_user_id(request):
    partner_id = int(request.GET.get('partnerId'))
    my_user_id = request.user.id
    return Response(
        ChatSerializer(
            get_object_or_404(Chat,
                Q(user1=my_user_id) & Q(user2=partner_id)
                                       | Q(user1=partner_id) & Q(user2=my_user_id)
            )
        ).data
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def post_talk(request):
    chat = Chat.objects.get(id=int(json.loads(request.body).get('chat')))
    talker = request.user
    sentence = json.loads(request.body).get('sentence')
    talk = Talk(talker=talker, chat=chat, sentence=sentence)
    talk.save()
    chat.talk_set.add(talk)
    chat.save()
    talk_reciever = chat.user2 if chat.user1 == talker else chat.user1
    chat_unread_counts = ChatUnreadTalkCount.objects.filter(user=talk_reciever, chat=chat)
    if(chat_unread_counts.count() == 0):
        chat_unread_count : ChatUnreadTalkCount = ChatUnreadTalkCount.objects.create(user=talk_reciever, chat=chat, count=1)
    else:
        chat_unread_count : ChatUnreadTalkCount = chat_unread_counts[0]
        chat_unread_count.increment()

    notify_talk_recieve(sender=talker, reciever=talk_reciever)

    return Response(
        TalkSerializer(
            talk
        ).data
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_chat_unread_total_count(request):
    chat_unread_total_count_model = ChatUnreadTalkCount.objects.filter(user=request.user)
    chat_unread_total_count = sum(map(lambda x:x.count, chat_unread_total_count_model))
    return Response(
       data={'chat_unread_total_count': chat_unread_total_count}, status=200,
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_chat_unread_count(request):
    chat_id = json.loads(request.body).get('chatId')
    auth_user = request.user
    chat = get_object_or_404(Chat,
                             id=chat_id)
    chat_unread_count : ChatUnreadTalkCount = get_object_or_404(ChatUnreadTalkCount, user=auth_user, chat=chat)
    chat_unread_count.reset()
    return Response(status=200)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_chat_list_for_chat_list_page(request):
    auth_user = request.user
    my_chat_list = Chat.objects.filter(
        Q(user2=auth_user) | Q(user1=auth_user)
    ).order_by('-updated_at')
    custom_chat_list = []
    for chat in my_chat_list:
        talk_list = Talk.objects.filter(
            chat=chat)
        if talk_list.count() == 0:
            continue
        latest_talk = talk_list.order_by('-created_at')[0]
        chat_unread_talk_count_model = ChatUnreadTalkCount.objects.filter(user=auth_user, chat=chat).first()
        if chat_unread_talk_count_model is not None:
            chat_unread_talk_count = chat_unread_talk_count_model.count
        else:
            chat_unread_talk_count = 0
        partner = chat.user2 if chat.user1 == request.user else chat.user1
        custom_chat = {'chat': ChatSerializer(chat).data,
                       'auth_user': request.user.id,
                       'partner': RestrictedUserSerializer(partner).data,
                       'created_at': chat.created_at,
                       'latest_talk': TalkSerializer(latest_talk).data,
                       'chat_unread_talk_count': chat_unread_talk_count}
        custom_chat_list.append(custom_chat)
    return Response(
        data=custom_chat_list, status=200
    )

"""
@login_required
def delete_talk(request):
    talk_id = request.POST.get('talk_id')
    talk = Talk.objects.get(id=talk_id)
    if request.user == talk.talker:
        talk.delete()
        d = {
            'talk_id': talk_id
        }
        return JsonResponse(d)
    else:
        return JsonResponse({'status':'false'}, status=500)

"""
