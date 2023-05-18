from rest_framework import serializers

from apps.login.models import LostAndFound


class LostAndFoundModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostAndFound
        fields = ['id', 'name', 'time', 'place', 'state', 'user_id', 'publish_time']
