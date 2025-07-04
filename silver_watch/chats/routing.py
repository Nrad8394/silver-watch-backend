from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<conversation_id>[a-f0-9\-]+)/$", ChatConsumer.as_asgi()),
]
