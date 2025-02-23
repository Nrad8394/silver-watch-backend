from django.contrib import admin
from .models import SystemSettings, APIKey, Webhook, UserPreferences

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ("site_name", "timezone", "language", "backup_schedule", "auto_update")

@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "last_used")

@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ("url", "active")

@admin.register(UserPreferences)
class UserPreferencesAdmin(admin.ModelAdmin):
    list_display = ("user", "theme", "dashboard_layout")
