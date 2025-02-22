from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()


class Alert(models.Model):
    ALERT_TYPES = [("Emergency", "Emergency"), ("Warning", "Warning"), ("Info", "Info")]
    ALERT_CATEGORIES = [("Health", "Health"), ("Device", "Device"), ("System", "System"), ("Security", "Security")]
    PRIORITY_LEVELS = [("High", "High"), ("Medium", "Medium"), ("Low", "Low")]
    STATUS_CHOICES = [("Active", "Active"), ("Acknowledged", "Acknowledged"), ("Resolved", "Resolved")]
    SOURCE_TYPES = [("Device", "Device"), ("System", "System"), ("User", "User")]
    TARGET_TYPES = [("Patient", "Patient"), ("Device", "Device"), ("System", "System")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type = models.CharField(max_length=10, choices=ALERT_TYPES)
    category = models.CharField(max_length=10, choices=ALERT_CATEGORIES)
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="Active")
    timestamp = models.DateTimeField(auto_now_add=True)

    source_type = models.CharField(max_length=10, choices=SOURCE_TYPES)
    source_id = models.CharField(max_length=255)
    source_name = models.CharField(max_length=255)

    target_type = models.CharField(max_length=10, choices=TARGET_TYPES)
    target_id = models.CharField(max_length=255)
    target_name = models.CharField(max_length=255)

    message = models.TextField()
    details = models.JSONField(default=dict, blank=True)

    acknowledgement_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="acknowledged_alerts")
    acknowledgement_at = models.DateTimeField(null=True, blank=True)
    acknowledgement_notes = models.TextField(null=True, blank=True)

    resolution_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="resolved_alerts")
    resolution_at = models.DateTimeField(null=True, blank=True)
    resolution_action = models.TextField(null=True, blank=True)
    resolution_notes = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"[{self.type}] {self.message} - {self.status}"


class NotificationChannel(models.Model):
    CHANNEL_TYPES = [("Email", "Email"), ("SMS", "SMS"), ("Push", "Push")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notification_channels")
    type = models.CharField(max_length=10, choices=CHANNEL_TYPES)
    enabled = models.BooleanField(default=True)
    target = models.CharField(max_length=255)  # Email or phone number
    verified = models.BooleanField(default=False)

    class Meta:
        unique_together = ("user", "type")

    def __str__(self):
        return f"{self.user.username} - {self.type} ({'Verified' if self.verified else 'Unverified'})"


class AlertRule(models.Model):
    OPERATORS = [(">", ">"), ("<", "<"), (">=", ">="), ("<=", "<="), ("=", "="), ("!=", "!=")]
    ACTION_TYPES = [("Notification", "Notification"), ("Email", "Email"), ("SMS", "SMS"), ("API", "API")]
    PRIORITY_LEVELS = [("High", "High"), ("Medium", "Medium"), ("Low", "Low")]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    metric = models.CharField(max_length=100)
    operator = models.CharField(max_length=2, choices=OPERATORS)
    value = models.FloatField()
    duration = models.IntegerField(null=True, blank=True)  # Duration in seconds
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS)
    enabled = models.BooleanField(default=True)

    actions = models.JSONField()  # List of actions
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_alert_rules")
    updated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="updated_alert_rules")

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.name} - {self.metric} {self.operator} {self.value}"
