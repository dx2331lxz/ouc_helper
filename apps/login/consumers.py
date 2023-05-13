from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
from apps.login.models import *
from asgiref.sync import sync_to_async
from channels.layers import get_channel_layer
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


def creat_roomid(u1, u2):
    if u1 > u2:
        return str(u2) + str(u1)
    else:
        return str(u1) + str(u2)


class ChatConsumer(AsyncWebsocketConsumer):

    async def websocket_connect(self, message):

        user_id = self.scope["url_route"]['kwargs'].get("id")

        # async_to_sync(Channel.objects.filter(user_id=user_id).update(channel_name=self.channel_name))
        # print(user_id)
        # print(self.scope)
        await self.accept()
        self.list = await self.save_channel(user_id)
        if len(self.list) != 0:
            for message in self.list:
                await self.send(message)

        # await self.channel_layer.group_add("group", self.channel_name)

    @database_sync_to_async
    def save_channel(self, user_id):
        message_list = []
        if Channel.objects.filter(user_id=user_id):
            if not Message.objects.filter(to_user=user_id):
                print(user_id)
            else:
                # channel_layer = get_channel_layer()
                for message in Message.objects.filter(to_user=user_id):
                    print(message.content)
                    message_list.append(message.content)
                    # channel_layer.send(message.room_id, str({'msg': message.content, 'room_id': message.room_id}))
            Channel.objects.filter(user_id=user_id).update(channel_name=self.channel_name, status=True)
        else:
            Channel.objects.create(user_id=user_id, channel_name=self.channel_name, status=True)
        Message.objects.filter(to_user=user_id).delete()
        return message_list

    async def websocket_receive(self, message):
        user_id = self.scope["url_route"]['kwargs'].get("id")
        group_id = await self.get_name(user_id)
        await self.get_status(group_id, message)
        await self.channel_layer.group_send(group_id, {"type": "send_message", "message": message})

    @database_sync_to_async
    def get_name(self, user_id):
        return Channel.objects.filter(user_id=user_id).first().group_id

    # 保存聊天记录（未发送到的）
    @database_sync_to_async
    def get_status(self, group_id, message):
        from_user = '0'
        to_user = '0'
        is_save = 0
        for obj in Channel.objects.filter(group_id=group_id):
            if obj.status == 1:
                from_user = obj.user_id
            else:
                is_save = 1
                to_user = obj.user_id
        if is_save:
            Message.objects.create(room_id=group_id, from_user=from_user, to_user=to_user, content=message['text'])

    async def send_message(self, event):
        text = event['message']['text']
        print(text)
        await self.send(text)

    async def websocket_disconnect(self, message):
        # group = self.scope["url_route"]['kwargs'].get("group")
        self.group_id = await self.change_channel(self.channel_name)
        await self.channel_layer.group_discard(self.group_id, self.channel_name)
        # group = await self.channel_layer.group_status(self.group_id)
        # await self.delete_group()

        print('离开了')
        raise StopConsumer()

    @database_sync_to_async
    def change_channel(self, channel_name):
        group_id = Channel.objects.filter(channel_name=channel_name).first().group_id
        Channel.objects.filter(channel_name=channel_name).update(status=False)
        return group_id

    # @database_sync_to_async
    # def delete_group(self):
    #     for i in Channel.objects.filter(group_id=self.group_id):
    #         if i.status == 1:
    #             return
    #     Channel.objects.filter(group_id=self.group_id).delete()
    #     print('删除成功')
