from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from apps.login.models import *
from asgiref.sync import sync_to_async

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
#
#
# class ChatConsumer(WebsocketConsumer):
#     def websocket_connect(self, message):
#         self.accept()
#         # group = self.scope["url_route"]['kwargs'].get("group")
#         group = '521'
#         async_to_sync(self.channel_layer.group_add)("group", self.channel_name)
#
#     def websocket_receive(self, message):
#         # group = self.scope["url_route"]['kwargs'].get("group")
#         group = '521'
#         async_to_sync(self.channel_layer.group_send)("group", {"type": "send_message", "message": message})
#
#     def send_message(self, event):
#         text = event['message']['text']
#         print(text)
#         self.send(text)
#
#     def websocket_disconnect(self, message):
#         # group = self.scope["url_route"]['kwargs'].get("group")
#         group = '521'
#         async_to_sync(self.channel_layer.group_discard)("group", self.channel_name)
#         raise StopConsumer()
from channels.generic.websocket import AsyncWebsocketConsumer


class ChatConsumer(AsyncWebsocketConsumer):

    async def websocket_connect(self, message):

        user_id = self.scope["url_route"]['kwargs'].get("id")
        await self.save_channel(user_id)

        # async_to_sync(Channel.objects.filter(user_id=user_id).update(channel_name=self.channel_name))
        # print(user_id)
        # print(self.scope)
        await self.accept()
        await self.channel_layer.group_add("group", self.channel_name)

    @database_sync_to_async
    def save_channel(self, user_id):
        if Channel.objects.filter(user_id=user_id):
            Channel.objects.filter(user_id=user_id).update(channel_name=self.channel_name)
        else:
            Channel.objects.create(user_id=user_id, channel_name=self.channel_name)

    async def websocket_receive(self, message):
        # group = self.scope["url_route"]['kwargs'].get("group")
        group = '521'

        await self.channel_layer.group_send("group", {"type": "send_message", "message": message})

    async def send_message(self, event):
        text = event['message']['text']
        print(text)
        await self.send(text)

    async def websocket_disconnect(self, message):
        # group = self.scope["url_route"]['kwargs'].get("group")
        group = '521'
        await self.channel_layer.group_discard("group", self.channel_name)
        print('离开了')
        raise StopConsumer()
