from rest_framework import routers
from .views import ReportViewSet
from . import views
from django.urls import path 


router = routers.DefaultRouter()
router.register(r'', ReportViewSet)

app_name = 'report'

# urlpatterns = [
#     path('report', views.ReportsViewSet.create, name='report')
# ]

