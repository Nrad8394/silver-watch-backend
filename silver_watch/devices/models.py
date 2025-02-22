from django.db import models
from django.contrib.auth import get_user_model
from datetime import datetime
import shortuuid
import uuid
User = get_user_model()

class Device(models.Model):
    TYPE_CHOICES = [
        ("Heart Monitor", "Heart Monitor"),
        ("Temperature Sensor", "Temperature Sensor"),
        ("Motion Sensor", "Motion Sensor"),
        ("Blood Pressure Monitor", "Blood Pressure Monitor"),
        ("Wearable Device", "Wearable Device"),
    ]
    
    STATUS_CHOICES = [
        ("Online", "Online"),
        ("Offline", "Offline"),
        ("Warning", "Warning"),
        ("Critical", "Critical"),
    ]
    # ID with dynamically set year prefix
    id = models.CharField(
        max_length=20, primary_key=True, unique=True, editable=False
    )
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default="Offline")
    battery_level = models.FloatField(default=100)
    signal_strength = models.FloatField(default=100)
    last_maintenance = models.DateTimeField(default=None, null=True, blank=True)
    next_maintenance = models.DateTimeField(default=None, null=True, blank=True)
    location = models.CharField(max_length=255,default=None, null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,limit_choices_to={'role': 'patient'})

    # Firmware details
    firmware_version = models.CharField(max_length=50,default=None, null=True, blank=True)
    firmware_last_update = models.DateTimeField(default=None, null=True, blank=True)
    firmware_available_update = models.CharField(max_length=50, null=True, blank=True)

    # Calibration details
    last_calibrated = models.DateTimeField(default=None, null=True, blank=True)
    next_calibration = models.DateTimeField(default=None, null=True, blank=True)
    calibration_accuracy = models.FloatField(default=None, null=True, blank=True)
    calibration_status = models.CharField(
        max_length=20, 
        choices=[("Calibrated", "Calibrated"), 
                 ("Needs Calibration", "Needs Calibration"), 
                 ("In Progress", "In Progress")],
        default="Needs Calibration"
    )

    def __str__(self):
        return f"{self.type} ({self.id}) - {self.status}"

    def save(self, *args, **kwargs):
        """Ensure ID is generated dynamically with the current year as a prefix."""
        if not self.id:
            year_prefix = str(datetime.now().year)
            unique_part = shortuuid.ShortUUID(alphabet="1234567890").random(length=10)
            self.id = f"{year_prefix}{unique_part}"  
        super().save(*args, **kwargs)
    class Meta:
        ordering = ["-status", "type"]  # Orders by status (descending) and then type (ascending)

class DeviceSettings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.OneToOneField(Device, on_delete=models.CASCADE, related_name="settings")
    sensitivity = models.FloatField(default=0.5)
    threshold = models.FloatField(default=0.5)
    sample_rate = models.FloatField(default=1.0)
    auto_calibration = models.BooleanField(default=False)
    high_precision_mode = models.BooleanField(default=False)
    error_compensation = models.BooleanField(default=False)
    
    alert_thresholds = models.JSONField(default=dict)  # Stores min/max alert values dynamically

    def __str__(self):
        return f"Settings for {self.device.type} ({self.device.id})"
    class Meta:
        ordering = ["device"]  # Orders by device ID

class DeviceMaintenance(models.Model):
    TYPE_CHOICES = [
        ("Calibration", "Calibration"),
        ("Battery Replacement", "Battery Replacement"),
        ("Firmware Update", "Firmware Update"),
        ("Hardware Check", "Hardware Check"),
    ]

    STATUS_CHOICES = [
        ("Scheduled", "Scheduled"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("Failed", "Failed"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="maintenance_records")
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default="Hardware Check")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Scheduled")
    scheduled_for = models.DateTimeField(default=None, null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    technician = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,limit_choices_to={'role': 'technician'})
    notes = models.TextField(null=True, blank=True)
    results = models.JSONField(null=True, blank=True)  # Stores success/failure details, before/after readings

    def __str__(self):
        return f"{self.type} for {self.device.type} ({self.device.id}) - {self.status}"
    class Meta:
        ordering = ["-scheduled_for"]  # Orders by latest scheduled maintenance first


class DeviceReading(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="readings")
    timestamp = models.DateTimeField(auto_now_add=True)
    reading_type = models.CharField(max_length=100)  # E.g., Heart Rate, Temperature
    value = models.FloatField()
    unit = models.CharField(max_length=20)  # E.g., bpm, °C, mmHg

    def __str__(self):
        return f"{self.reading_type} - {self.value}{self.unit} ({self.device.id})"

    class Meta:
        ordering = ["-timestamp"]  # Orders by most recent readings first