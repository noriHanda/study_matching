from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import Report
from .serializers import ReportSerializer


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        reporting_user_id = int(request.user.id)
        reported_user_id = int(request.data.get('reported_user_id'))
        content = request.data.get('content')
        if reporting_user_id != reported_user_id:
            if reporting_user_id and reported_user_id:
                if content is not None:
                    report = ReportSerializer(Report.objects.create(
                        reporting_user_id=reporting_user_id,
                        reported_user_id=reported_user_id,
                        content=content,
                    )).data
                    if report is not None:
                        return Response({'message': '通報が完了しました。'}, status=201)
                else:
                    return Response({'message': '内容を入力してください。'}, status=400)

        return Response(status=400, data={'errorCode': 'DEFAULT_BAD_REQUEST'})
