from rest_framework import routers
from .views import TagViewSet
from . import views
from django.urls import path

router = routers.DefaultRouter()
router.register(r'', TagViewSet)

app_name = 'tag'

urlpatterns = [
    path('fetch_user_having_tags', views.fetch_user_having_tags, name='fetch_user_having_tags'),
]

