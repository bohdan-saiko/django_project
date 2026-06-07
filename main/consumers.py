import json
from channels.generic.websocket import AsyncWebsocketConsumer

class OnlineConsumer(AsyncWebsocketConsumer):
    online_connections = set()
    group_name = "online_users"

    async def connect(self):
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()
        
        OnlineConsumer.online_connections.add(self.channel_name)
        await self.broadcast_count()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)
        
        OnlineConsumer.online_connections.discard(self.channel_name)
        await self.broadcast_count()

    async def broadcast_count(self):
        current_count = len(OnlineConsumer.online_connections)
        
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "send_count_to_client",
                "count": current_count
            }
        )

    async def send_count_to_client(self, event):
        await self.send(text_data=json.dumps({
            "online_count": event["count"]
        }))