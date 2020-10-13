from rest_framework import routers
from .views import UserBlockViewSet
from . import views
from django.urls import path

router = routers.DefaultRouter()
router.register(r'', UserBlockViewSet)

app_name = 'user_block'

urlpatterns = [
    path('fetch_user_block_list', views.fetch_user_block_list, name='fetch_user_block_list'),
    path('unblock', views.unblock, name='unblock'),
]

