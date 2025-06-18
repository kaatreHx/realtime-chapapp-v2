# from channels.generic.websocket import AsyncWebsocketConsumer
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async
from .models import CustomUser
from channels.exceptions import StopConsumer


class MyAsyncConsumer(AsyncConsumer):

    async def websocket_connect(self,event):
        print("WebSocket connected...", event)
        # print("User in scope:", self.scope['user'], self.scope['user'].is_authenticated)
        user = self.scope['user']
        print(user.name)
        if user.is_authenticated:
            await self.set_user_online(user.id)
        
        print(self.scope['url_route']['kwargs']['groupName'])
        
        self.channel_layer.group_add("come from param", self.channel_name)

        await self.send({
            'type': 'websocket.accept'
        })

        # await self.close()

    async def websocket_disconnect(self, event):
        print("WebSocket disconnected...", event)
        user = self.scope['user']
        if user.is_authenticated:
            await self.set_user_offline(user.id)
        
        self.channel_layer.group_discard("come from param", self.channel_name)
        raise StopConsumer()

    async def websocket_receive(self, event):
        print("Message from client:", event)  
        # await self.send(text_data = "Helloworld")
        print('Actual Data .. ', event['message'])
        print('Type of Actual Data .. ', type(event['message']))
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })
    
    async def chat_message(self, event):
        print('Event .. ', event)
        print('Actual Data .. ', event['message'])
        print('Type of Actual Data .. ', type(event['message']))
        await self.send({
            'type': 'websocket.send',
            'text': event['message']
        })

    @database_sync_to_async
    def set_user_online(self, user_id):
        CustomUser.objects.filter(id=user_id).update(online_status=True)

    @database_sync_to_async
    def set_user_offline(self, user_id):
        CustomUser.objects.filter(id=user_id).update(online_status=False)
