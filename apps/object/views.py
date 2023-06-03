from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.login import models
from .serializer import LostAndFoundModelSerializer

from django.views.decorators.csrf import csrf_exempt
import base64
from ouc_helper import settings
import requests
from django.utils.decorators import method_decorator
from uuid import uuid1
import json
import os
# Create your views here.


class InformationView(APIView):

    def get(self, request):
        data = request.query_params.dict()
        id = data['id']
        obj = models.LostAndFound.objects.filter(id=id)
        objs_s = LostAndFoundModelSerializer(instance=obj, many=True)
        user = models.Information.objects.filter(user_id=objs_s.data[0]['user']).first()
        objs_s.data[0]['user_name'] = user.name
        objs_s.data[0]['avatar'] = f'{settings.SITE_DOMAIN}{user.avatar_url.url}'
        pictures = models.Picture.objects.filter(thing_id=id)
        picture_data = []
        for picture in pictures:
            picture_data.append(f'{settings.SITE_DOMAIN}{picture.url.url}')
        objs_s.data[0]['pictures'] = picture_data
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
        return JsonResponse({'code': 200, 'message': 'OK', 'data': {'thing_id': obj_s.data['id']}})


class InformationDeleteView(APIView):

    def post(self, request):
        data = json.loads(request.body.decode())
        id = data['id']
        user_id = request.user.id
        if not models.LostAndFound.objects.filter(id=id, user_id=user_id).exists():
            return JsonResponse({'code': 404, 'message': '该记录不存在或不是当前登录用户发布'})
        pictures = models.Picture.objects.filter(thing_id=id)
        for picture in pictures:
            os.remove(picture.url.path)
            picture.delete()
        models.LostAndFound.objects.filter(id=id, user_id=user_id).first().delete()
        return JsonResponse({'code': 200, 'message': 'OK'})

# # 上传图片到GitHub
# def save_to_github(filename, content):
#     url = f"{settings.GITHUB_API_URL}/repos/{settings.GITHUB_OWNER}/{settings.GITHUB_REPO}/contents/{filename}"
#     headers = {
#         'Authorization': f'token {settings.GITHUB_TOKEN}',
#         'Content-Type': 'application/json'
#     }
#     data = {
#         'message': f'Add {filename}',
#         'content': content,
#         'branch': settings.GITHUB_BRANCH
#     }
#     response = requests.put(url, headers=headers, json=data)
#     if response.status_code == 201:
#         return True
#     return False
#
#
#
#
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class UploadImageView(APIView):
#     def post(self, request):
#         if request.FILES:
#             thing_id = request.POST.get('thing_id')
#             # print(thing_id)
#             image_files = request.FILES.getlist('image')
#             # print(image_files)
#             image_urls = []
#             for image_file in image_files:
#                 file_format = image_file.name.split('.')[-1]
#                 filename = 'ouchelper/' + f'{uuid1().hex}.{file_format}'
#                 # print('filemane', filename)
#                 content = base64.b64encode(image_file.file.read()).decode('utf-8')
#                 if save_to_github(filename, content):
#                     # image_url = f"https://raw.githubusercontent.com/{settings.GITHUB_OWNER}/{settings.GITHUB_REPO}/{settings.GITHUB_BRANCH}/{filename}"
#                     image_url = f"https://picture.daoxuan.cc/{filename}"
#                     models.Picture.objects.create(thing_id=thing_id, url=image_url)
#                     image_urls.append(image_url)
#                 else:
#                     return JsonResponse({'code': 400, 'message': 'Failed to upload image'})
#                 data = {
#                  'url': image_urls,
#                 }
#             return JsonResponse({'code': 200, 'message': 'OK', 'data': data})
#         else:
#             return JsonResponse({'code': 403, 'message': 'Unsupported file format'})


class UploadImageAPIView(APIView):
    def post(self, request):
        if request.FILES:
            thing_id = request.POST.get('thing_id')
            # print(thing_id)
            user_id = request.user.id
            if models.LostAndFound.objects.filter(id=thing_id).first().user_id != user_id:
                return JsonResponse({'code': 405, 'message': '该物品不是当前用户发布'})
            image_files = request.FILES.getlist('image')
            # print(image_files)
            image_urls = []
            for image_file in image_files:
                if image_file.size > 1 * 1024 * 1024:
                    return JsonResponse({'code': 402, 'message': '上传文件过大'})
                else:
                    picture = models.Picture.objects.create(thing_id=thing_id)
                    picture.url = image_file
                    picture.save()
                    image_urls.append(f'{settings.SITE_DOMAIN}{picture.url.url}')
            return JsonResponse({'code': 200, 'url': image_urls})
        else:
            return JsonResponse({'code': 401, 'message': '请传图片'})
