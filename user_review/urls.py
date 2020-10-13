from rest_framework import routers
from .views import UserReviewViewSet

router = routers.DefaultRouter()
router.register(r'', UserReviewViewSet)

from django.urls import path
from . import views

app_name = 'user_review'

urlpatterns = [
    path('fetch_my_created_reviews', views.fetch_my_created_reviews, name='fetch_my_created_reviews'),
    path('fetch_reviews_to_user', views.fetch_reviews_to_user, name='fetch_reviews_to_user'),
]
