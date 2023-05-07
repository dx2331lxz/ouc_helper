from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('register/', views.RegisterAPIView.as_view()),
    path('code/', views.EmailVerificationAPIView.as_view()),
]