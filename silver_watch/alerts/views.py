from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Alert, NotificationChannel, AlertRule
from .serializers import AlertSerializer, NotificationChannelSerializer, AlertRuleSerializer

class AlertViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == "patient":
            return self.queryset.filter(target_id=self.request.user.id, target_type="Patient")
        return self.queryset


class NotificationChannelViewSet(viewsets.ModelViewSet):
    queryset = NotificationChannel.objects.all()
    serializer_class = NotificationChannelSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class AlertRuleViewSet(viewsets.ModelViewSet):
    queryset = AlertRule.objects.all()
    serializer_class = AlertRuleSerializer
    permission_classes = [IsAuthenticated]
