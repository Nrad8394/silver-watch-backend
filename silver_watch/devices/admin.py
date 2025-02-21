from django.contrib import admin
from .models import Device, DeviceSettings, DeviceMaintenance, DeviceReading

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ("id", "type", "status", "battery_level", "assigned_to", "location", "next_maintenance")
    search_fields = ("type", "assigned_to__username", "location")
    list_filter = ("status", "type")
    readonly_fields = ("firmware_version", "firmware_last_update")

@admin.register(DeviceSettings)
class DeviceSettingsAdmin(admin.ModelAdmin):
    list_display = ("device", "sensitivity", "threshold", "sample_rate", "auto_calibration")
    search_fields = ("device__id",)
    list_filter = ("auto_calibration", "high_precision_mode")

@admin.register(DeviceMaintenance)
class DeviceMaintenanceAdmin(admin.ModelAdmin):
    list_display = ("device", "type", "status", "scheduled_for", "completed_at", "technician")
    search_fields = ("device__id", "technician__username")
    list_filter = ("status", "type")

@admin.register(DeviceReading)
class DeviceReadingAdmin(admin.ModelAdmin):
    list_display = ("device", "timestamp", "reading_type", "value", "unit")
    search_fields = ("device__id", "reading_type")
    list_filter = ("reading_type",)

