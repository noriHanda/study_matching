from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import MethodNotAllowed
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes

from .models import UserBlock
from .serializers import UserBlockSerializer
from django.shortcuts import get_object_or_404


class UserBlockViewSet(viewsets.ModelViewSet):
    queryset = UserBlock.objects.all()
    serializer_class = UserBlockSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        blocked_user_id = int(request.data.get('blocked_user_id'))
        blocking_user_id = int(request.user.id)
        if blocking_user_id != blocked_user_id:
            if blocking_user_id and blocked_user_id:
                if UserBlock.objects.filter(
                        blocking_user_id=blocking_user_id, blocked_user_id=blocked_user_id).count() == 0:
                    user_block_data = UserBlockSerializer(UserBlock.objects.create(
                        blocking_user_id=blocking_user_id,
                        blocked_user_id=blocked_user_id,
                    )).data
                    if user_block_data:
                        return Response(user_block_data, status=201)
                else:
                    return Response(status=400, data={'errorCode': 'A_USER_CANNOT_CREATE_MULTIPLE_BLOCKS_FOR_ONE_USER'})

        return Response(status=400, data={'errorCode': 'DEFAULT_BAD_REQUEST'})

    def update(self, request, pk=None, *args, **kwargs):
        return Response(status=MethodNotAllowed.status_code, data={'details: Method PUT not allowed.'})

    def partial_update(self, request, pk=None, *args, **kwargs):
        return Response(status=MethodNotAllowed.status_code, data={'details: Method PATCH not allowed.'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_user_block_list(request):
    blocking_user = request.user
    return Response(
        UserBlockSerializer(
            UserBlock.objects.filter(
                blocking_user=blocking_user
            ),
            many=True
        ).data
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def unblock(request):
    blocking_user = request.user
    blocked_user_id = int(request.data.get('blocked_user_id'))
    print(blocked_user_id)
    print("test")
    user_block = get_object_or_404(UserBlock,
        blocking_user=blocking_user, blocked_user__id=blocked_user_id)
    user_block.delete()
    return Response(data={'message': 'unblocked successfully'}, status=200)
