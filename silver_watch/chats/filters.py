import django_filters
from .models import Conversation, Message, Contact

class ConversationFilter(django_filters.FilterSet):
    participants = django_filters.CharFilter(method="filter_by_participant")
    type = django_filters.ChoiceFilter(choices=Conversation.CONVERSATION_TYPES)

    def filter_by_participant(self, queryset, name, value):
        return queryset.filter(participants__id=value)

    class Meta:
        model = Conversation
        fields = ["participants", "type"]


class MessageFilter(django_filters.FilterSet):
    conversation = django_filters.UUIDFilter(field_name="conversation__id")
    sender = django_filters.UUIDFilter(field_name="sender__id")
    recipient = django_filters.UUIDFilter(field_name="recipient__id")
    type = django_filters.ChoiceFilter(choices=Message.MESSAGE_TYPES)
    read = django_filters.BooleanFilter()

    class Meta:
        model = Message
        fields = ["conversation", "sender", "recipient", "type", "read"]


class ContactFilter(django_filters.FilterSet):
    user = django_filters.UUIDFilter(field_name="user__id")
    status = django_filters.ChoiceFilter(choices=Contact.STATUS_CHOICES)
    department = django_filters.CharFilter(lookup_expr="icontains")

    class Meta:
        model = Contact
        fields = ["user",  "status", "department"]
