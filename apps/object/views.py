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
        obj = models.LostAndFound.objects.filter(id=id)
        objs_s = LostAndFoundModelSerializer(instance=obj, many=True)
        user = models.Information.objects.filter(user_id=objs_s.data[0]['user']).first()
        objs_s.data[0]['user_name'] = user.name
        objs_s.data[0]['avator'] = user.avator_url
        pictures = models.Picture.objects.filter(thing_id=id)
        picture_data = []
        for picture in pictures:
            picture_data.append(picture.url)
        objs_s.data[0]['picture'] = picture_data
        contact = {
            'phone': user.phone,
            'qq': user.qq,
            'wechat': user.wechat,
        }
        objs_s.data[0]['contact'] = contact
        return JsonResponse({'code': 200, 'message': 'OK', 'data': objs_s.data[0]})

    def post(self, request):
        data = json.loads(request.body.decode())
        data['user'] = request.user.id
        obj_s = LostAndFoundModelSerializer(data=data)
        if not obj_s.is_valid(raise_exception=True):
            return JsonResponse({'code': 400, 'message': '参数不正确'})
        obj_s.save()
        return JsonResponse({'code': 200, 'message': 'OK'})


class InformationDeleteView(APIView):

    def post(self, request):
        data = json.loads(request.body.decode())
        id = data['id']
        user_id = request.user.id
        if not models.LostAndFound.objects.filter(id=id, user_id=user_id).exists():
            return JsonResponse({'code': 404, 'message': '该记录不存在或不是当前登录用户发布'})
        models.LostAndFound.objects.filter(id=id, user_id=user_id).first().delete()
        return JsonResponse({'code': 200, 'message': 'OK'})
