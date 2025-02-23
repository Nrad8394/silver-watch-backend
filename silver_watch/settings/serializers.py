from rest_framework import serializers
from .models import SystemSettings, APIKey, Webhook, UserPreferences

class APIKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = APIKey
        fields = "__all__"

class WebhookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webhook
        fields = "__all__"

class SystemSettingsSerializer(serializers.ModelSerializer):
    api_keys = APIKeySerializer(many=True, read_only=True)
    webhooks = WebhookSerializer(many=True, read_only=True)

    class Meta:
        model = SystemSettings
        fields = "__all__"

class UserPreferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPreferences
        fields = "__all__"
