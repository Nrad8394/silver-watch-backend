from django.contrib import admin
from .models import Conversation, Message, Contact

class MessageInline(admin.TabularInline):  
    model = Message  
    extra = 0  
    readonly_fields = ("sender", "recipient", "content", "timestamp", "read", "type")  
    ordering = ("-timestamp",)  

@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "participants_list", "created_at", "updated_at", "last_message_preview")
    list_filter = ("type", "created_at")
    search_fields = ("participants__username", "group_name")
    readonly_fields = ("created_at", "updated_at")
    inlines = [MessageInline]

    def participants_list(self, obj):
        return ", ".join([user.username for user in obj.participants.all()])
    participants_list.short_description = "Participants"

    def last_message_preview(self, obj):
        last_msg = obj.last_message()
        return last_msg.content[:50] if last_msg else "No messages"
    last_message_preview.short_description = "Last Message"

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("id", "conversation", "sender", "recipient", "type", "timestamp", "read")
    list_filter = ("type", "read", "timestamp")
    search_fields = ("sender__username", "recipient__username", "content")
    readonly_fields = ("timestamp",)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name",  "status", "last_seen")
    list_filter = ( "status", "last_seen")
    search_fields = ("user__username", "name", "department", "specialization")
    readonly_fields = ("last_seen",)
