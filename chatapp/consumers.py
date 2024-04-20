import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, Room

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        self.room_name = f"room_{self.scope['url_route']['kwargs']['room_name']}"
        await self.channel_layer.group_add(self.room_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        message = json.loads(text_data)

        event = {
            'type': "send_message",
            'message': message
        }
        await self.create_message(data=message)
        await self.channel_layer.group_send(self.room_name, event)

    async def send_message(self, event):
        data = event['message']
        response_data = {
            'sender': data['sender'],
            'message': data['message']
        }
        await self.send(text_data=json.dumps({'message': response_data}))

    @database_sync_to_async
    def create_message(self, data):
        Message.objects.create(
            user=data['sender'],
            room=Room.objects.get(name=data['room_name']),
            text=data['message']
        )