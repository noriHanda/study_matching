from . import views
from django.urls import path

app_name = 'search'

urlpatterns = [path('offers/tags', views.search_offer_with_tags, name='search_offer_with_tags')]
