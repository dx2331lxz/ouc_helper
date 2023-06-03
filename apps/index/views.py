from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from apps.login import models
from .serializer import LostAndFoundModelSerializer
from ouc_helper import settings

import json
# Create your views here.


class page(PageNumberPagination):

    page_size = 5
    max_page_size = 10
    page_size_query_param = 'page_size'


class IndexView(APIView):

    permission_classes = [AllowAny]
    pagination_class = page

    def get(self, request):
        data = request.query_params.dict()
        type = data['type']
        objs = models.LostAndFound.objects.filter(type=type)
        paginated_objs = self.pagination_class().paginate_queryset(objs, request)
        objs_s = LostAndFoundModelSerializer(instance=paginated_objs, many=True)
        for datas in objs_s.data:
            user = models.Information.objects.filter(user_id=datas['user_id']).first()
            pictures = models.Picture.objects.filter(thing_id=datas['id']).order_by('id')[:3]
            datas['user_name'] = user.name
            datas['user_avatar'] = f'{settings.SITE_DOMAIN}{user.avatar_url.url}'
            picture_data = []
            for picture in pictures:
                picture_data.append(f'{settings.SITE_DOMAIN}{picture.url.url}')
            datas['pictures'] = picture_data
        return JsonResponse({'code': 200, 'message': 'OK', 'data': objs_s.data})








