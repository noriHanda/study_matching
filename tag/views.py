from rest_framework import viewsets

from .models import Tag
from .serializers import TagSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import MethodNotAllowed


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        return Response(status=MethodNotAllowed.status_code, data={'details: Method POST not allowed.'})

    def update(self, request, pk=None, *args, **kwargs):
        return Response(status=MethodNotAllowed.status_code, data={'details: Method PUT not allowed.'})

    def partial_update(self, request, pk=None, *args, **kwargs):
        return Response(status=MethodNotAllowed.status_code, data={'details: Method PATCH not allowed.'})

    def destroy(self, request, pk=None, *args, **kwargs):
        return Response(status=MethodNotAllowed.status_code, data={'details: Method DELETE not allowed.'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_user_having_tags(request):
    user_id = int(request.GET.get('user_id'))
    return Response(
        TagSerializer(
            Tag.objects.filter(
                users__id=user_id
            ),
            many=True
        ).data
    )

