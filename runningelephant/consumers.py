from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ProfileConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        self.room_group_name = 'profile'
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )
    
    async def chat_message(self, event):
        #if self.user.username == event['message']:
        message = ' New Broadcast: ' + event['message']
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
