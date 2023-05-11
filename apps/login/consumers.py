from channels.generic.websocket import WebsocketConsumer
from channels.exceptions import StopConsumer
# from asgiref.sync import async_to_sync
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
        await self.accept()
        # group = self.scope["url_route"]['kwargs'].get("group")
        group = '521'
        await self.channel_layer.group_add("group", self.channel_name)

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
        raise StopConsumer()
