from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView

from apps.login import models
from .serializer import LostAndFoundModelSerializer

import json
# Create your views here.


class InformationView(APIView):

    def get(self, request):
        data = json.loads(request.body.decode())
        id = data['id']
        obj = models.LostAndFound.objects.filter(id=id).first()
        objs_s = LostAndFoundModelSerializer(instance=obj)
        user = models.Information.objects.filter(user_id=objs_s.data['user_id']).first()
        objs_s.data['user_name'] = user.name
        objs_s.data['avator'] = user.avator_url
        pictures = models.Picture.objects.filter(thing_id=objs_s.data['id'])
        picture_data = []
        for picture in pictures:
            picture_data.append(picture.url)
        objs_s.data['picture'] = picture_data
        contact = {
            'phone': user.phone,
            'qq': user.qq,
            'email': user.email,
        }
        objs_s.data['contact'] = contact
        objs_s.data.pop('type')
        return JsonResponse({'code': 200, 'message': 'OK', 'data': objs_s.data})

    def post(self, request):
        data = json.loads(request.body.decode())
        data['user_id'] = request.user.id
        obj_s = LostAndFoundModelSerializer(data=data)
        if not obj_s.is_valid(raise_exception=True):
            return JsonResponse({'code': 400, 'message': '参数不正确'})
        obj_s.save()
        return JsonResponse({'code': 200, 'message': 'OK'})


class InformationDeleteView(APIView):

    def post(self, request):
        data = json.loads(request.body.decode())
        id = data['id']
        models.LostAndFound.objects.filter(id=id).first().delete()
        return JsonResponse({'code': 200, 'message': 'OK'})
