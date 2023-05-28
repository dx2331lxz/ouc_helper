from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from apps.login.models import *
from .serializer import *
from rest_framework.response import Response
from rest_framework import status
# 上传github图床
from django.views.decorators.csrf import csrf_exempt
import base64
from ouc_helper import settings
import requests
from uuid import uuid1
from django.http import JsonResponse
from django.utils.decorators import method_decorator
import json
import os

# class AddAvatorAPIView(APIView):
#     def post(self, request):
#         user_id = request.user.id
#         data = request.data
#         avator_url = data['url']
#         if not Information.objects.filter(user_id=user_id):
#             Information.objects.create(avator_url=avator_url, user_id=user_id)
#         else:
#             Information.objects.filter(user_id=user_id).update(avator_url=avator_url)
#         result = {'msg': '添加成功', 'code': 200}
#         return Response(result, status=status.HTTP_200_OK)


class GetAPIView(APIView):
    def get(self, request):
        user_id = request.user.id
        instance = Information.objects.filter(user_id=user_id).first()
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

    def get(self, request):
        user_id = request.user.id
        if not Information.objects.filter(user_id=user_id):
            Information.objects.create(user_id=user_id)
        name = Information.objects.filter(user_id=user_id).first().name
        return Response({'msg': name, 'code': 200}, status=status.HTTP_200_OK)


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

    def get(self, request):
        user_id = request.user.id
        if not Information.objects.filter(user_id=user_id):
            Information.objects.create(user_id=user_id)
        phone = Information.objects.filter(user_id=user_id).first().phone
        return Response({'msg': phone, 'code': 200}, status=status.HTTP_200_OK)


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

    def get(self, request):
        user_id = request.user.id
        if not Information.objects.filter(user_id=user_id):
            Information.objects.create(user_id=user_id)
        qq = Information.objects.filter(user_id=user_id).first().qq
        return Response({'msg': qq, 'code': 200}, status=status.HTTP_200_OK)


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

    def get(self, request):
        user_id = request.user.id
        if not Information.objects.filter(user_id=user_id):
            Information.objects.create(user_id=user_id)
        wechat = Information.objects.filter(user_id=user_id).first().wechat
        return Response({'msg': wechat, 'code': 200}, status=status.HTTP_200_OK)


# 上传头像
# class AddAvatorAPIView(APIView):
#     def post(self, request, format=None):
#         user_id = request.user.id
#         base64_str = request.data.get('file')
#         if not base64_str:
#             return Response({'message': 'File not found.'}, status=status.HTTP_400_BAD_REQUEST)
#
#         # 解码 base64 编码的图片数据
#         try:
#             file_data = base64.b64decode(base64_str)
#         except:
#             return Response({'message': 'Invalid base64 data.'}, status=status.HTTP_400_BAD_REQUEST)
#
#         if len(file_data) > 10 * 1024 * 1024:
#             return Response({'message': 'File size too large. Maximum file size is 10MB.'},
#                             status=status.HTTP_400_BAD_REQUEST)
#
#         filename = 'ouchelper/' + hashlib.md5((str(time.time())).encode('utf-8')).hexdigest() + '.jpg'
#
#         access_key = 'z0zDuhtssmdi7XgvfzEffyPAqyVIHRPv8_ju6X-M'
#         secret_key = 'ALrTgAlRwaKi9Vu7juFVhuiFV9PIfQTPuaB9FmDi'
#         bucket_name = 'daoxuan-image'
#
#         q = Auth(access_key, secret_key)
#         token = q.upload_token(bucket_name, filename, 3600)
#         ret, info = put_data(token, filename, file_data)
#         ex = 'https://image.daoxuan.cc/(.*)'
#
#         if info.status_code == 200:
#             file_url = 'https://image.daoxuan.cc' + '/' + filename
#             if Information.objects.filter(user_id=user_id):
#                 file_key = Information.objects.filter(user_id=user_id)[0].avatar
#                 if file_key != None:
#                     file_key = re.findall(ex, file_key)
#                     file_key = file_key[0]
#                     photo_delete.photo_delete(file_key)
#                 Information.objects.filter(user_id=user_id).update(avatar_url=file_url)
#             else:
#                 Information.objects.create(user_id=user_id, avatar_url=file_url)
#
#             return Response({'file_url': file_url})
#         else:
#             return Response({'message': 'File upload failed.'}, status=status.HTTP_400_BAD_REQUEST)

# def get(self, request):
#     user_id = request.user.id
#     if not Information.objects.filter(user_id=user_id):
#         return Response({'msg': '头像未上传'})
#     file_url = Information.objects.filter(user_id=user_id)[0].avator_url
#     return Response({'file_url': file_url}, status=status.HTTP_200_OK)


# 上传图片到GitHub
# @csrf_exempt
# def save_to_github(filename, content):
#     url = f"{settings.GITHUB_API_URL}/repos/{settings.GITHUB_OWNER}/{settings.GITHUB_REPO}/contents/{filename}"
#     headers = {
#         'Host': 'api.github.com',
#         'Authorization': f'token {settings.GITHUB_TOKEN}',
#         'Accept': 'application / vnd.github.v3+json'
#     }
#     data = {
#         'message': f'Add {filename}',
#         'committer': {
#             'name': f'{settings.GITHUB_OWNER}',
#             'email': "3434055686@qq.com"
#         },
#         'content': content,
#         'branch': settings.GITHUB_BRANCH,
#         "path": filename
#     }
#     response = requests.put(url, headers=headers, json=data)
#
#     print(response.text)
#     if response.status_code == 201:
#         return True
#     return False
#
#
# @method_decorator(csrf_exempt, name='dispatch')
# class UploadImageAPIView(APIView):
#     def post(self, request):
#         if request.FILES:
#             user_id = request.user.id
#             image_file = request.FILES.get('image')
#             file_format = image_file.name.split('.')[-1]
#             filename = 'ouchelper/' + f'{uuid1().hex}.{file_format}'
#             # print('filemane', filename)
#             content = base64.b64encode(image_file.file.read()).decode('utf-8')
#             if save_to_github(filename, content):
#                 # image_url = f"https://raw.githubusercontent.com/{settings.GITHUB_OWNER}/{settings.GITHUB_REPO}/{settings.GITHUB_BRANCH}/{filename}"
#                 image_url = f"https://picture.daoxuan.cc/{filename}"
#                 if Information.objects.filter(user_id=user_id):
#                     Information.objects.filter(user_id=user_id).update(avatar_url=image_url)
#                 else:
#                     Information.objects.create(user_id=user_id, avatar_url=image_url)
#                 data = {
#                     'success': True,
#                     'url': image_url,
#                 }
#                 return Response(data)
#             else:
#                 data = {
#                     'success': False,
#                     'message': 'Failed to upload image'
#                 }
#                 return Response(data)
#         else:
#             data = {
#                 'success': False,
#                 'message': 'Unsupported file format'
#             }
#             return Response(data)
#
#     def get(self, request):
#         user_id = request.user.id
#         information = Information.objects.filter(user_id=user_id)
#         if information:
#             avatar_url = information.first().avatar_url
#             return Response({'msg': avatar_url, 'code': 200}, status=status.HTTP_200_OK)
#         else:
#             obj = Information.objects.create(user_id=user_id)
#             avatar_url = obj.avatar_url
#             return Response({'msg': avatar_url, 'code': 200}, status=status.HTTP_200_OK)


class UploadImageAPIView(APIView):
    def post(self, request):
        user_id = request.user.id
        data = request.data
        image = data.get('image','')
        print(image)
        if image == '':
            return Response('请传图片')
        elif image.size >  1 * 1024 * 1024:
            return Response('上传文件过大')
        else:
            if not Information.objects.filter(user_id=user_id):
                Information.objects.create(user_id=user_id)
                information = Information.objects.filter(user_id=user_id).first()
                information.avatar_url = image
                information.save()
            else:
                information = Information.objects.filter(user_id=user_id).first()
                os.remove(information.avatar_url.path)
                print(information.avatar_url.path)
                information.avatar_url = image
                information.save()
            return Response({'url':f'{settings.SITE_DOMAIN}{information.avatar_url.url}'})
    def get(self, request):
        user_id = request.user.id
        if not Information.objects.filter(user_id=user_id):
            Information.objects.create(user_id=user_id)
        else:
            return Response({'url':f'{settings.SITE_DOMAIN}{Information.objects.filter(user_id=user_id).first().avatar_url.url}'})

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
                picture_data.append(f'{settings.SITE_DOMAIN}{picture.url.url}')
            datas['pictures'] = picture_data
        return JsonResponse({'code': 200, 'message': 'OK', 'data': objs_s.data})
