from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ('reporting_user_id', 'reported_user_id', 'content', 'created_at')
