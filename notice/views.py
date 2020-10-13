from django.contrib.auth.decorators import login_required
from .models import Notice, UnreadNoticeCount
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import NoticeSerializer


@api_view(['GET'])
@login_required
def fetch_my_notice_list(request):
    notice_list = Notice.objects.filter(recieved_user=request.user).order_by('-created_at')
    return Response(NoticeSerializer(notice_list, many=True).data)


@api_view(['POST'])
@login_required
def reset_my_unread_notice_count(request):
    unread_notice_count_model = UnreadNoticeCount.objects.filter(user=request.user).first()
    unread_notice_count_model.reset()
    return JsonResponse({'details': 'お知らせの未読数のリセットに成功しました。'}, status=200)


@api_view(['GET'])
@login_required
def fetch_my_unread_notice_count(request):
    unread_notice_count = UnreadNoticeCount.objects.filter(user=request.user).first().count
    return Response(data={'unread_notice_count': unread_notice_count}, status=200)
