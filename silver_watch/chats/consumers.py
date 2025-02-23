import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from .models import Conversation, Message

logger = logging.getLogger(__name__)

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            self.conversation_id = self.scope["url_route"]["kwargs"]["conversation_id"]
            self.room_group_name = f"chat_{self.conversation_id}"

            # Check if the conversation exists
            exists = await sync_to_async(Conversation.objects.filter(id=self.conversation_id).exists)()
            if not exists:
                await self.close()
                return

            # Add to the group
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
        except Exception as e:
            logger.error(f"WebSocket connection error: {str(e)}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        except Exception as e:
            logger.error(f"WebSocket disconnect error: {str(e)}")
    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
            message_text = data.get("message")
            sender_id = data.get("sender")

            if not message_text or not sender_id:
                await self.send(json.dumps({"error": "Invalid message data"}))
                return

            # Validate sender
            sender = await sync_to_async(User.objects.filter(id=sender_id).first)()
            if not sender:
                await self.send(json.dumps({"error": "Sender not found"}))
                return

            # Get conversation
            conversation = await sync_to_async(Conversation.objects.filter(id=self.conversation_id).first)()
            if not conversation:
                await self.send(json.dumps({"error": "Conversation not found"}))
                return

            # Determine recipient (for individual chat)
            if conversation.type == Conversation.INDIVIDUAL:
                recipient = await sync_to_async(lambda: conversation.participants.exclude(id=sender.id).first())()
                if not recipient:
                    await self.send(json.dumps({"error": "Recipient not found"}))
                    return
            else:
                recipient = None  # For group chats, there is no single recipient

            # Save message to database
            message = await sync_to_async(Message.objects.create)(
                conversation=conversation,
                sender=sender,
                recipient=recipient,  # ✅ Fix: Set recipient for individual chats
                content=message_text
            )

            # Broadcast message
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "chat_message",
                    "message": message_text,
                    "sender": sender_id,
                    "recipient": recipient.id if recipient else None,  # Include recipient
                    "timestamp": str(message.timestamp),
                },
            )
        except json.JSONDecodeError:
            await self.send(json.dumps({"error": "Invalid JSON format"}))
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}")
            await self.send(json.dumps({"error": "Internal server error"}))

    async def chat_message(self, event):
        try:
            await self.send(text_data=json.dumps(event))
        except Exception as e:
            logger.error(f"Error sending message: {str(e)}")
