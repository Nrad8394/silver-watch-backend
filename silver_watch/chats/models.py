import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class Conversation(models.Model):
    INDIVIDUAL = "individual"
    GROUP = "group"
    CONVERSATION_TYPES = [(INDIVIDUAL, "Individual"), (GROUP, "Group")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    participants = models.ManyToManyField(User, related_name="conversations")
    type = models.CharField(max_length=20, choices=CONVERSATION_TYPES, default=INDIVIDUAL)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    group_name = models.CharField(max_length=255, blank=True, null=True)
    group_avatar = models.URLField(blank=True, null=True)
    admins = models.ManyToManyField(User, related_name="group_admins", blank=True)

    def last_message(self):
        return self.messages.order_by("-timestamp").first()

    def unread_count_for_user(self, user):
        return self.messages.filter(recipient=user, read=False).count()

    def __str__(self):
        return f"Conversation ({self.get_type_display()})"

class Message(models.Model):
    TEXT = "text"
    IMAGE = "image"
    FILE = "file"
    MESSAGE_TYPES = [(TEXT, "Text"), (IMAGE, "Image"), (FILE, "File")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages",
                            limit_choices_to=models.Q(conversations__isnull=False))
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages",
                              limit_choices_to=models.Q(conversations__isnull=False), blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    type = models.CharField(max_length=10, choices=MESSAGE_TYPES, default=TEXT)

    file_name = models.CharField(max_length=255, blank=True, null=True)
    file_size = models.PositiveIntegerField(blank=True, null=True)
    mime_type = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient} ({self.get_type_display()})"

class Contact(models.Model):

    ONLINE = "Online"
    OFFLINE = "Offline"
    AWAY = "Away"
    STATUS_CHOICES = [(ONLINE, "Online"), (OFFLINE, "Offline"), (AWAY, "Away")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="contact")
    name = models.CharField(max_length=255)
    avatar = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=OFFLINE)
    last_seen = models.DateTimeField(auto_now=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
