from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('index/', views.ChatAPIView.as_view()),
    path('add/', views.AddRoomAPIView.as_view()),
]