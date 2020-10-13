from . import views
from django.urls import path

app_name = 'notice'

urlpatterns = [
    path('reset_my_unread_notice_count/', views.reset_my_unread_notice_count, name='reset_my_unread_notice_count'),
    path('fetch_my_notice_list/', views.fetch_my_notice_list, name='fetch_my_notice_list'),
    path('fetch_my_unread_notice_count/', views.fetch_my_unread_notice_count, name='fetch_my_unread_notice_count'),

]