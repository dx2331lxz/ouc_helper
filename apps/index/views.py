from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from apps.login import models
from .serializer import LostAndFoundModelSerializer

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
        data = json.loads(request.body.decode())
        type = data['type']
        objs = models.LostAndFound.objects.filter(type=type)
        paginated_objs = self.pagination_class().paginate_queryset(objs, request)
        objs_s = LostAndFoundModelSerializer(instance=paginated_objs, many=True)
        for datas in objs_s.data:
            user = models.Information.objects.filter(user_id=datas['user_id']).first()
            pictures = models.Picture.objects.filter(thing_id=datas['id']).order_by('id')[:3]
            datas['user_name'] = user.name
            datas['user_picture'] = user.avator_url
            picture_data = []
            for picture in pictures:
                picture_data.append(picture.url)
            datas['picture'] = picture_data
        return JsonResponse({'code': 200, 'message': 'OK', 'data': objs_s.data})








