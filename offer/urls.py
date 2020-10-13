from rest_framework import routers
from .views import OfferViewSet
from . import views
from django.urls import path

router = routers.DefaultRouter()
router.register(r'', OfferViewSet)

app_name = 'offer'

urlpatterns = [
    path('fetch_user_offer_set_list', views.fetch_user_offer_set_list, name='fetch_user_offer_set_list'),
    path('fetch_user_offer_set_list_logged_out', views.fetch_user_offer_set_list_logged_out, name='fetch_user_offer_set_list_logged_out'),
    path('fetch_individual_user_offer_list', views.fetch_individual_user_offer_list, name='fetch_individual_user_offer_list'),
]
