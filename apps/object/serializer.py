from rest_framework import serializers

from apps.login.models import LostAndFound


class LostAndFoundModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostAndFound
        fields = '__all__'
