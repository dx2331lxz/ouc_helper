from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # path('avatar/add/', views.upload_image),
    path('avatar/', views.UploadImageAPIView.as_view()),
    path('name/', views.AddNameAPIView.as_view()),
    path('phone/', views.AddPhoneAPIView.as_view()),
    path('qq/', views.AddQQAPIView.as_view()),
    path('wechat/', views.AddWechatAPIView.as_view()),
    path('get/', views.GetAPIView.as_view()),
    path('object/', views.PersonObjectView.as_view()),
    # path('avatar/get/', views.AvatarGetAPIView.as_view())
]