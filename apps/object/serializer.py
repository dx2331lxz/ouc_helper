from rest_framework import serializers

from apps.login.models import LostAndFound, Picture


class LostAndFoundModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = LostAndFound
        fields = '__all__'
        # fields = ['name', 'time', 'place', 'description', 'state', 'user_id']

class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'