from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class VitalSigns(models.Model):
    STATUS_CHOICES = [("Normal", "Normal"), ("Warning", "Warning"), ("Critical", "Critical")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vital_signs", limit_choices_to={'role': 'patient'})
    timestamp = models.DateTimeField(auto_now_add=True)

    heart_rate = models.FloatField()
    heart_rate_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Normal")

    blood_pressure_systolic = models.FloatField()
    blood_pressure_diastolic = models.FloatField()
    blood_pressure_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Normal")

    temperature = models.FloatField()
    temperature_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Normal")

    blood_oxygen = models.FloatField()
    blood_oxygen_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Normal")

    respiratory_rate = models.FloatField()
    respiratory_rate_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Normal")

    consciousness_value = models.IntegerField()
    consciousness_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Normal")

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"Vitals for {self.patient} - {self.timestamp}"


class HealthMetrics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="health_metrics", limit_choices_to={'role': 'patient'})
    date = models.DateField()
    steps = models.IntegerField(default=0)
    active_minutes = models.IntegerField(default=0)
    heart_rate_zone_minutes = models.IntegerField(default=0)
    calories_burned = models.FloatField(default=0.0)
    distance_walked = models.FloatField(default=0.0)
    sleep_hours = models.FloatField(default=0.0)

    class Meta:
        ordering = ["-date"]

    def __str__(self):
        return f"Metrics for {self.patient} - {self.date}"


class MedicalHistory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="medical_history", limit_choices_to={'role': 'patient'})

    conditions = models.JSONField(default=list)
    allergies = models.JSONField(default=list)
    surgeries = models.JSONField(default=list)
    medications = models.JSONField(default=list)

    def __str__(self):
        return f"Medical History for {self.patient}"


class HealthTrend(models.Model):
    METRIC_CHOICES = [
        ("heart_rate", "Heart Rate"),
        ("blood_pressure", "Blood Pressure"),
        ("temperature", "Temperature"),
        ("blood_oxygen", "Blood Oxygen"),
        ("respiratory_rate", "Respiratory Rate"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="health_trends", limit_choices_to={'role': 'patient'})
    metric = models.CharField(max_length=20, choices=METRIC_CHOICES)
    data = models.JSONField(default=list)  # Stores historical data points
    range_min = models.FloatField()
    range_max = models.FloatField()
    unit = models.CharField(max_length=10)

    def __str__(self):
        return f"Trend for {self.patient} - {self.metric}"
