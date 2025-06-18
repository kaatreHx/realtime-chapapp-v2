from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/as/', consumers.MyAsyncConsumer.as_asgi())
]