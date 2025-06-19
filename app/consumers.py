from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import CustomUser
import re
import json


class MyAsyncConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        print("WebSocket connected...")

        self.user = self.scope['user']
        print("User:", self.user.name)

        if self.user.is_authenticated:
            await self.set_user_online(self.user.id)

        self.receiver = self.scope['url_route']['kwargs'].get('name')

        if self.receiver is None:
            print("Receiver name not provided in URL.")
            self.receiver = "default"

        print("Receiver:", self.receiver)

        self.group = self.get_group_name(self.user, self.receiver)
        print("Group:", self.group)

        await self.channel_layer.group_add(self.group, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        print("WebSocket disconnected...")

        if self.user.is_authenticated:
            await self.set_user_offline(self.user.id)

        await self.channel_layer.group_discard(self.group, self.channel_name)

    async def receive(self, text_data):
        print("Message from client:", text_data)

        await self.channel_layer.group_send(self.group, {
            'type': 'chat_message',
            'message': text_data,
            'user': self.user.name
        })

    async def chat_message(self, event):
        print("Event:", event)

        # Assuming `event['message']` is a JSON string like '{"msg":"Hello"}'
        # Parse it to extract just the message text
        message_dict = json.loads(event['message'])  # extract "Hello"
        actual_message = message_dict.get("msg", "")

        # Format it as "manish: Hello"
        final_message = f"{event['user']}: {actual_message}"

        await self.send(text_data=final_message)


    @database_sync_to_async
    def set_user_online(self, user_id):
        CustomUser.objects.filter(id=user_id).update(online_status=True)

    @database_sync_to_async
    def set_user_offline(self, user_id):
        CustomUser.objects.filter(id=user_id).update(online_status=False)

    def get_group_name(self, user, receiver):
        names = sorted([user.name, receiver])
        raw = f"chat_{names[0]}_{names[1]}"
        safe = re.sub(r'[^a-zA-Z0-9_.-]', '_', raw)
        return safe[:100]
