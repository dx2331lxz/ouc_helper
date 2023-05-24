from django.urls import path
from . import views

urlpatterns = [
    path('information/', views.InformationView.as_view()),
    path('delete/', views.InformationDeleteView.as_view()),
    path('addpictures/', views.UploadImageView.as_view()),
]
