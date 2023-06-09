from rest_framework import serializers
from apps.login.models import *
from rest_framework_simplejwt.serializers import TokenObtainSerializer, TokenObtainPairSerializer
from rest_framework import exceptions


class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Information
        fields = "__all__"


class LostAndFoundModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostAndFound
        fields = ['id', 'name', 'time', 'place', 'state']
