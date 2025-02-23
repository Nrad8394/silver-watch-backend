from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Conversation, Message, Contact
from .serializers import ConversationSerializer, MessageSerializer, ContactSerializer
from .filters import ConversationFilter, MessageFilter, ContactFilter
from .mixins import UserOwnedMixin

class ConversationViewSet(UserOwnedMixin, viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ConversationFilter
    search_fields = ["group_name"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-updated_at"]
    model_name = "conversation"  # Define for Mixin


class MessageViewSet(UserOwnedMixin, viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = MessageFilter
    search_fields = ["content"]
    ordering_fields = ["timestamp"]
    ordering = ["-timestamp"]
    model_name = "message"  # Define for Mixin


class ContactViewSet(UserOwnedMixin, viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ContactFilter
    search_fields = ["name", "department", "specialization"]
    ordering_fields = ["last_seen"]
    ordering = ["-last_seen"]
    model_name = "contact"  # Define for Mixin
