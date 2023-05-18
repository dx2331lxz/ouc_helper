from rest_framework import serializers

from apps.login.models import LostAndFound


class LostAndFoundModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostAndFound
        fields = '__all__'
        # fields = ['name', 'time', 'place', 'description', 'state', 'user_id']
