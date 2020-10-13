from rest_framework import routers
from .views import ChatViewSet
from .views import TalkViewSet

from . import views
from django.urls import path

chat_router = routers.DefaultRouter()
chat_router.register(r'', ChatViewSet)

talk_router = routers.DefaultRouter()
talk_router.register(r'', TalkViewSet)


app_name = 'chat'

urlpatterns = [
    path('search_chat', views.search_chat, name='search_chat'),
    path('fetch_my_chat', views.fetch_my_chat, name='fetch_my_chat'),
    path('fetch_latest_talk', views.fetch_latest_talk, name='fetch_latest_talk'),
    path('fetch_all_talk', views.fetch_all_talk, name='fetch_all_talk'),
    path('fetch_chat_with_user_id', views.fetch_chat_with_user_id, name='fetch_chat_with_user_id'),
    path('post_talk', views.post_talk, name='post_talk'),
    path('fetch_chat_unread_total_count/', views.fetch_chat_unread_total_count, name='fetch_chat_unread_total_count'),
    path('reset_chat_unread_count', views.reset_chat_unread_count, name='reset_chat_unread_count'),
    path('fetch_chat_list_for_chat_list_page',
         views.fetch_chat_list_for_chat_list_page,
         name='fetch_chat_list_for_chat_list_page'),
]

