from rest_framework import serializers
from .models import HealthReport, DeviceReport, AnalyticsData, Incident, MedicationAdherence, MaintenanceRecord, DeviceIssue, Trend, TrendDataPoint

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = "__all__"

class MedicationAdherenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicationAdherence
        fields = "__all__"

class HealthReportSerializer(serializers.ModelSerializer):
    incidents = IncidentSerializer(many=True, read_only=True)
    medications = MedicationAdherenceSerializer(many=True, read_only=True)

    class Meta:
        model = HealthReport
        fields = "__all__"

class MaintenanceRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaintenanceRecord
        fields = "__all__"

class DeviceIssueSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceIssue
        fields = "__all__"

class DeviceReportSerializer(serializers.ModelSerializer):
    maintenance_records = MaintenanceRecordSerializer(many=True, read_only=True)
    issues = DeviceIssueSerializer(many=True, read_only=True)

    class Meta:
        model = DeviceReport
        fields = "__all__"

class TrendDataPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrendDataPoint
        fields = "__all__"

class TrendSerializer(serializers.ModelSerializer):
    data_points = TrendDataPointSerializer(many=True, read_only=True)

    class Meta:
        model = Trend
        fields = "__all__"

class AnalyticsDataSerializer(serializers.ModelSerializer):
    trends = TrendSerializer(many=True, read_only=True)

    class Meta:
        model = AnalyticsData
        fields = "__all__"
