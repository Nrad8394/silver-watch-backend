from django.contrib import admin
from .models import HealthReport, Incident, MedicationAdherence, DeviceReport, MaintenanceRecord, DeviceIssue, AnalyticsData, Trend, TrendDataPoint

@admin.register(HealthReport)
class HealthReportAdmin(admin.ModelAdmin):
    list_display = ("patient", "report_type", "start_date", "end_date", "generated_at")

@admin.register(DeviceReport)
class DeviceReportAdmin(admin.ModelAdmin):
    list_display = ("device_id", "start_date", "end_date", "uptime")

@admin.register(AnalyticsData)
class AnalyticsDataAdmin(admin.ModelAdmin):
    list_display = ("timeframe", "active_users", "total_patients", "critical_alerts")

admin.site.register([Incident, MedicationAdherence, MaintenanceRecord, DeviceIssue, Trend, TrendDataPoint])
