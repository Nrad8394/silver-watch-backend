import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class HealthReport(models.Model):
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"
    CUSTOM = "Custom"
    REPORT_TYPES = [(DAILY, "Daily"), (WEEKLY, "Weekly"), (MONTHLY, "Monthly"), (CUSTOM, "Custom")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="health_reports")
    report_type = models.CharField(max_length=10, choices=REPORT_TYPES, default=DAILY)
    start_date = models.DateField()
    end_date = models.DateField()
    generated_at = models.DateTimeField(auto_now_add=True)
    generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="generated_reports")

    # Vital Stats
    heart_rate_avg = models.FloatField()
    heart_rate_min = models.FloatField()
    heart_rate_max = models.FloatField()
    heart_rate_out_of_range = models.IntegerField()

    systolic_avg = models.FloatField()
    diastolic_avg = models.FloatField()
    blood_pressure_out_of_range = models.IntegerField()

    temperature_avg = models.FloatField()
    temperature_out_of_range = models.IntegerField()

    blood_oxygen_avg = models.FloatField()
    blood_oxygen_out_of_range = models.IntegerField()

    # Activity Stats
    total_steps = models.IntegerField()
    active_minutes = models.IntegerField()
    resting_hours = models.FloatField()

    def __str__(self):
        return f"{self.patient} - {self.report_type} Report ({self.start_date} - {self.end_date})"

class Incident(models.Model):
    report = models.ForeignKey(HealthReport, on_delete=models.CASCADE, related_name="incidents")
    timestamp = models.DateTimeField()
    type = models.CharField(max_length=255)
    severity = models.CharField(max_length=50)
    description = models.TextField()

class MedicationAdherence(models.Model):
    report = models.ForeignKey(HealthReport, on_delete=models.CASCADE, related_name="medications")
    name = models.CharField(max_length=255)
    adherence = models.FloatField()
    missed = models.IntegerField()
class DeviceReport(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device_id = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    uptime = models.FloatField()

    connectivity_quality = models.FloatField()
    connectivity_disconnections = models.IntegerField()

    battery_avg_level = models.FloatField()
    battery_charge_cycles = models.IntegerField()

    def __str__(self):
        return f"Device {self.device_id} Report ({self.start_date} - {self.end_date})"

class MaintenanceRecord(models.Model):
    report = models.ForeignKey(DeviceReport, on_delete=models.CASCADE, related_name="maintenance_records")
    type = models.CharField(max_length=255)
    date = models.DateField()
    outcome = models.TextField()
    technician = models.CharField(max_length=255)

class DeviceIssue(models.Model):
    report = models.ForeignKey(DeviceReport, on_delete=models.CASCADE, related_name="issues")
    timestamp = models.DateTimeField()
    type = models.CharField(max_length=255)
    resolution = models.TextField(blank=True, null=True)

class DeviceReading(models.Model):
    report = models.ForeignKey(DeviceReport, on_delete=models.CASCADE, related_name="readings")
    total = models.IntegerField()
    invalid = models.IntegerField()
    accuracy = models.FloatField()
class AnalyticsData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    timeframe = models.CharField(max_length=50)
    active_users = models.IntegerField()
    total_patients = models.IntegerField()
    critical_alerts = models.IntegerField()
    response_time = models.FloatField()
    device_utilization = models.FloatField()

    def __str__(self):
        return f"Analytics Report - {self.timeframe}"

class Trend(models.Model):
    analytics = models.ForeignKey(AnalyticsData, on_delete=models.CASCADE, related_name="trends")
    metric = models.CharField(max_length=255)

class TrendDataPoint(models.Model):
    trend = models.ForeignKey(Trend, on_delete=models.CASCADE, related_name="data_points")
    timestamp = models.DateTimeField()
    value = models.FloatField()

class Breakdown(models.Model):
    analytics = models.ForeignKey(AnalyticsData, on_delete=models.CASCADE, related_name="breakdowns")
    category = models.CharField(max_length=255)
    value = models.IntegerField()
