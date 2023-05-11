from django.urls import re_path

from apps.login import consumers

websocket_urlpatterns = {
    re_path(r'room/(?P<id>\w+)/$', consumers.ChatConsumer.as_asgi()),
}
