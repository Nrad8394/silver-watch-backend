from rest_framework import serializers
from .models import Conversation, Message, Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"

class ConversationSerializer(serializers.ModelSerializer):
    last_message = serializers.SerializerMethodField()
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = "__all__"

    def get_last_message(self, obj):
        last_msg = obj.last_message()
        if last_msg:
            return MessageSerializer(last_msg).data
        return None  # Return None if no messages exist

    def get_unread_count(self, obj):
        user = self.context["request"].user
        return obj.unread_count_for_user(user)
