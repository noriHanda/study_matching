from django.urls import path
from . import views

app_name = "firebase_messaging"

urlpatterns = [
    path('register/', views.RegisterFCMTokenView.as_view(), name='register'),
]
