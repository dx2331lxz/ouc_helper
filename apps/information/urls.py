from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('avator/add/', views.AddAvatorAPIView.as_view()),
    path('name/add/', views.AddNameAPIView.as_view()),
    path('phone/add/', views.AddPhoneAPIView.as_view()),
    path('qq/add/', views.AddQQAPIView.as_view()),
    path('wechat/add/', views.AddWechatAPIView.as_view()),
    path('get/', views.GetAPIView.as_view()),
    path('object/', views.PersonObjectView.as_view()),
]