from django.shortcuts import render
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class ChatAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        return render(request, 'chat.html')
