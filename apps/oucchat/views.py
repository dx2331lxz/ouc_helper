from django.shortcuts import render
from rest_framework.views import APIView
from apps.login.models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class ChatAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        id = request.GET.get('id')
        to_id = request.GET.get('to_id')
        return render(request, 'chat.html', {'id': id, 'to_id':to_id})


def creat_roomid(u1, u2):
    if u1 > u2:
        return str(u2) + str(u1)
    else:
        return str(u1) + str(u2)


class AddRoomAPIView(APIView):
    def post(self, request):
        user_id = request.user.id
        print(user_id)
        data = request.data
        to_id = data['to_id']
        # user_id = data['user_id']
        roomid = creat_roomid(int(to_id), int(user_id))
        channel_layer = get_channel_layer()
        from_channel_name = Channel.objects.filter(user_id=user_id).first().channel_name
        to_channel_name = Channel.objects.filter(user_id=to_id).first().channel_name
        async_to_sync(channel_layer.group_add)(roomid, from_channel_name)
        async_to_sync(channel_layer.group_add)(roomid, to_channel_name)
        # Channel.objects.filter(user_id__in=[user_id, to_id]).update(group_id=roomid)
        if Group.objects.filter(group_id=roomid):
            pass
        else:
            Group.objects.create(group_id=roomid, widget_user_ids=[int(user_id), int(to_id)])
        result = {"msg": "ok", "code": 200}
        return Response(result, status=status.HTTP_200_OK)
