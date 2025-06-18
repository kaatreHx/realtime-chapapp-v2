from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/as/(?P<name>[^/]+)/$', consumers.MyAsyncConsumer.as_asgi()),
    re_path(r'ws/as/', consumers.MyAsyncConsumer.as_asgi()),
]