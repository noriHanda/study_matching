from .models import FCMDeviceToken
from .serializers import FCMDeviseTokenSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated


class RegisterFCMTokenView(CreateAPIView):

    queryset = FCMDeviceToken.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = FCMDeviseTokenSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

