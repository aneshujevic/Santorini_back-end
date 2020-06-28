# chat/consumers.py
import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer

room_name = 'amphitheatre'


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Join room group
        await self.channel_layer.group_add(
            room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            room_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        # Send message to room group
        await self.channel_layer.group_send(
            room_name,
            {
                'type': 'chat_message',
                'message': text_data
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
