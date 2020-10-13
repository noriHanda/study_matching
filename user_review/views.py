from rest_framework import viewsets

from .models import UserReview
from .serializers import UserReviewSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

import json
from rest_framework.exceptions import MethodNotAllowed


class UserReviewViewSet(viewsets.ModelViewSet):
    queryset = UserReview.objects.all()
    serializer_class = UserReviewSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        reviewee_id = int(request.data.get('reviewee'))
        text = request.data.get('text')
        rating = int(request.data.get('rating'))
        reviewer_id = int(request.user.id)
        if reviewee_id != reviewer_id:
            if reviewee_id and reviewer_id:
                if UserReview.objects.filter(
                        reviewee_id=reviewee_id, reviewer_id=reviewer_id).count() == 0:
                    UserReview_data = UserReviewSerializer(UserReview.objects.create(
                        reviewee_id=reviewee_id,
                        reviewer_id=reviewer_id,
                        text=text,
                        rating=rating
                    )).data
                    if(UserReview_data):
                        return Response(UserReview_data, status=201)
                else:
                    return Response(status=400, data={'errorCode': 'A_USER_CANNOT_CREATE_MULTIPLE_REVIEWS_FOR_ONE_USER'})

        return Response(status=400, data={'errorCode': 'DEFAULT_BAD_REQUEST'})

    def update(self, request, pk=None, *args, **kwargs):
        return Response(status=MethodNotAllowed.status_code, data={'details: Method PUT not allowed.'})

    def partial_update(self, request, pk=None, *args, **kwargs):
        return Response(status=MethodNotAllowed.status_code, data={'details: Method PATCH not allowed.'})

    def destroy(self, request, pk=None, *args, **kwargs):
        return Response(status=MethodNotAllowed.status_code, data={'details: Method DELETE not allowed.'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_my_created_reviews(request):
    reviewer = request.user
    return Response(
        UserReviewSerializer(
            UserReview.objects.filter(
                reviewer=reviewer
            ),
            many=True
        ).data
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def fetch_reviews_to_user(request):
    reviewee_id = int(request.GET.get('userId'))
    return Response(
        UserReviewSerializer(
            UserReview.objects.filter(
                reviewee_id=reviewee_id
            ),
            many=True
        ).data
    )
