from django.contrib import admin
from .models import VitalSigns, HealthMetrics, MedicalHistory, HealthTrend

@admin.register(VitalSigns)
class VitalSignsAdmin(admin.ModelAdmin):
    list_display = ("patient", "timestamp", "heart_rate", "blood_pressure_systolic", "temperature")
    search_fields = ("patient__username", "timestamp")
    list_filter = ("timestamp", "heart_rate_status")

@admin.register(HealthMetrics)
class HealthMetricsAdmin(admin.ModelAdmin):
    list_display = ("patient", "date", "steps", "calories_burned")
    search_fields = ("patient__username", "date")

@admin.register(MedicalHistory)
class MedicalHistoryAdmin(admin.ModelAdmin):
    list_display = ("patient",)
    search_fields = ("patient__username",)

@admin.register(HealthTrend)
class HealthTrendAdmin(admin.ModelAdmin):
    list_display = ("patient", "metric", "range_min", "range_max")
    search_fields = ("patient__username", "metric")
