"""study_matching URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path

from offer.urls import router as offer_router
from tag.urls import router as tag_router
from chat.urls import talk_router
from chat.urls import chat_router
from account.urls import router as user_router
from user_review.urls import router as user_review_router
from account.views import UserActivationView
from account.views import password_reset_form_page
from user_block.urls import router as user_block_router
from report.urls import router as report_router
from account.custom_jwt_auth import CustomJWTTokenView


from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('djoser.urls')),
    re_path(r'^api/auth/users/activate/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$', UserActivationView.as_view()),
    re_path(r'^api/auth/users/reset_password_form_page/(?P<uid>[\w-]+)/(?P<token>[\w-]+)/$', password_reset_form_page),
    path('api/offers/', include(offer_router.urls)),
    path('api/tags/', include(tag_router.urls)),
    path('api/search/', include('search.urls')),
    path('api/users/', include(user_router.urls)),
    path('api/chats/', include(chat_router.urls)),
    path('api/talks/', include(talk_router.urls)),
    path('api/chat_utils/', include('chat.urls')),
    path('api/tag_utils/', include('tag.urls')),
    path('api/firebase_messaging/', include('firebase_messaging.urls')),
    path('api/offer_utils/', include('offer.urls')),
    path('api/user_reviews/', include(user_review_router.urls)),
    path('api/user_review_utils/', include('user_review.urls')),
    path('api/user_blocks/', include(user_block_router.urls)),
    path('api/user_block_utils/', include('user_block.urls')),
    path('api/reports/', include(report_router.urls)),
    path('api/notice_utils/', include('notice.urls')),
]

urlpatterns += [
    path('api/auth/', include('djoser.urls.jwt')),
    path('api/auth/jwt/create/', CustomJWTTokenView.as_view(), name="jwt-create"),
][1:]

if settings.DEBUG:
    urlpatterns += [
        path('api-auth/', include('rest_framework.urls')),
    ]
