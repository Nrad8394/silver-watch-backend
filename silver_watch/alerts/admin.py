from django.contrib import admin
from .models import Alert, NotificationChannel, AlertRule

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ("type", "category", "priority", "status", "timestamp")
    list_filter = ("status", "priority", "category")
    search_fields = ("message", "source_name", "target_name")


@admin.register(NotificationChannel)
class NotificationChannelAdmin(admin.ModelAdmin):
    list_display = ("user", "type", "target", "enabled", "verified")
    list_filter = ("type", "enabled", "verified")
    search_fields = ("user__username", "target")


@admin.register(AlertRule)
class AlertRuleAdmin(admin.ModelAdmin):
    list_display = ("name", "metric", "operator", "value", "priority", "enabled")
    list_filter = ("priority", "enabled")
    search_fields = ("name", "metric")
