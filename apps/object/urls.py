from django.urls import path
from . import views

urlpatterns = [
    path('information/', views.InformationView.as_view()),
    path('information/delete/', views.InformationDeleteView.as_view()),
]