from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from apps.login.models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework import status

import json

class AddAvatorAPIView(APIView):
    def post(self, request):
        user_id = request.user.id
        data = request.data
        avator_url = data['url']
        if not Information.objects.filter(user_id=user_id):
            Information.objects.create(avator_url=avator_url, user_id=user_id)
        else:
            Information.objects.filter(user_id=user_id).update(avator_url=avator_url)
        result = {'msg': '添加成功', 'code': 200}
        return Response(result, status=status.HTTP_200_OK)


class GetAPIView(APIView):
    def get(self, request):
        user_id = request.user.id
        instance = Information.objects.filter(user_id=user_id)
        serializer = InformationSerializer(instance=instance)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddNameAPIView(APIView):
    def post(self, request):
        user_id = request.user.id
        data = request.data
        name = data['name']
        if not Information.objects.filter(user_id=user_id):
            Information.objects.create(name=name, user_id=user_id)
        else:
            Information.objects.filter(user_id=user_id).update(name=name)
        result = {'msg': '添加成功', 'code': 200}
        return Response(result, status=status.HTTP_200_OK)


class AddPhoneAPIView(APIView):
    def post(self, request):
        user_id = request.user.id
        data = request.data
        phone = data['phone']
        if not Information.objects.filter(user_id=user_id):
            Information.objects.create(phone=phone, user_id=user_id)
        else:
            Information.objects.filter(user_id=user_id).update(phone=phone)
        result = {'msg': '添加成功', 'code': 200}
        return Response(result, status=status.HTTP_200_OK)


class AddQQAPIView(APIView):
    def post(self, request):
        user_id = request.user.id
        data = request.data
        qq = data['qq']
        if not Information.objects.filter(user_id=user_id):
            Information.objects.create(qq=qq, user_id=user_id)
        else:
            Information.objects.filter(user_id=user_id).update(qq=qq)
        result = {'msg': '添加成功', 'code': 200}
        return Response(result, status=status.HTTP_200_OK)


class AddWechatAPIView(APIView):
    def post(self, request):
        user_id = request.user.id
        data = request.data
        wechat = data['wechat']
        if not Information.objects.filter(user_id=user_id):
            Information.objects.create(wechat=wechat, user_id=user_id)
        else:
            Information.objects.filter(user_id=user_id).update(wechat=wechat)
        result = {'msg': '添加成功', 'code': 200}
        return Response(result, status=status.HTTP_200_OK)


class page(PageNumberPagination):

    page_size = 5
    max_page_size = 10
    page_size_query_param = 'page_size'


class PersonObjectView(APIView):

    pagination_class = page

    def get(self, request):
        data = json.loads(request.body.decode())
        type = data['type']
        id = request.user.id
        objs = LostAndFound.objects.filter(type=type, user_id=id)
        paginated_objs = self.pagination_class().paginate_queryset(objs, request)
        objs_s = LostAndFoundModelSerializer(instance=paginated_objs, many=True)
        for datas in objs_s.data:
            pictures = Picture.objects.filter(thing_id=datas['id']).order_by('id')[:3]
            picture_data = []
            for picture in pictures:
                picture_data.append(picture.url)
            datas['pictures'] = picture_data
        return JsonResponse({'code': 200, 'message': 'OK', 'data': objs_s.data})
