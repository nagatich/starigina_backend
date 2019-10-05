import asyncio
import json

from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

from channels.generic.websocket import AsyncJsonWebsocketConsumer

from .models import *
from .serializers import *

class Consumer(AsyncJsonWebsocketConsumer):
    
    room = None
    
    async def connect(self):
        try:
            token = self.scope['query_string'].decode("utf-8").replace('token=', '')
            user = Token.objects.get(key=token).user
            room = f"{user.username}_room"
            self.room = room
            if self.room:
                await self.accept()
                await self.channel_layer.group_add(self.room, self.channel_name)
                notifications = Notification.objects.filter(Q(to_user=user) & Q(seen=False))
                if notifications:
                    serializer = NotificationSerializer(instance=notifications, many=True)
                    await self.channel_layer.group_send(
                        self.room,
                        {
                            "type": "notificate",
                            "event": "notifications",
                            "data": serializer.data
                        }
                    )
            else:
                await self.close()
        except:
            await self.close()
        
    async def disconnect(self, code):
        if self.room is not None:
            await self.channel_layer.group_discard(self.room, self.channel_name)
        
    async def notificate(self, event):
        await self.send_json(event)
        
    async def receive(self, text_data):
        token = self.scope['query_string'].decode("utf-8").replace('token=', '')
        user = Token.objects.get(key=token).user
        data = json.loads(text_data)
        if 'notification' in data:
            notification = Notification.objects.get(pk=data['notification'])
            notification.seen = True
            notification.save()