import uuid
from django.db import models

class SystemSettings(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # General
    site_name = models.CharField(max_length=255, default="My System")
    timezone = models.CharField(max_length=100, default="UTC")
    language = models.CharField(max_length=50, default="en")
    date_format = models.CharField(max_length=50, default="YYYY-MM-DD")
    time_format = models.CharField(max_length=50, default="HH:mm")

    # Security
    session_timeout = models.IntegerField(default=30)  # in minutes
    password_min_length = models.IntegerField(default=8)
    password_require_numbers = models.BooleanField(default=True)
    password_require_symbols = models.BooleanField(default=False)
    password_require_uppercase = models.BooleanField(default=True)
    password_expiry_days = models.IntegerField(default=90)

    two_factor_required = models.BooleanField(default=False)
    two_factor_methods = models.JSONField(default=list)  # ["email", "sms", "authenticator"]
    ip_whitelist = models.JSONField(default=list)  # List of allowed IPs

    # Notifications
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    push_enabled = models.BooleanField(default=True)

    alert_throttling_enabled = models.BooleanField(default=True)
    alert_max_per_hour = models.IntegerField(default=10)
    alert_cooldown_minutes = models.IntegerField(default=5)

    # Maintenance
    backup_schedule = models.CharField(max_length=10, choices=[("daily", "Daily"), ("weekly", "Weekly"), ("monthly", "Monthly")], default="daily")
    backup_retention = models.IntegerField(default=30)  # Retention in days
    auto_update = models.BooleanField(default=True)

    maintenance_day = models.IntegerField(default=0)  # 0 = Sunday, 6 = Saturday
    maintenance_start_time = models.TimeField(default="02:00")
    maintenance_duration = models.IntegerField(default=60)  # In minutes

    # Integrations
    integrations_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"System Settings ({self.site_name})"

class APIKey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    system_settings = models.ForeignKey(SystemSettings, on_delete=models.CASCADE, related_name="api_keys")
    name = models.CharField(max_length=255)
    key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"API Key: {self.name}"

class Webhook(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    system_settings = models.ForeignKey(SystemSettings, on_delete=models.CASCADE, related_name="webhooks")
    url = models.URLField()
    events = models.JSONField()  # List of event names
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Webhook {self.url}"
from django.contrib.auth import get_user_model

User = get_user_model()

class UserPreferences(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="preferences")

    # Theme & Layout
    theme = models.CharField(max_length=10, choices=[("light", "Light"), ("dark", "Dark"), ("system", "System")], default="system")
    dashboard_layout = models.CharField(max_length=15, choices=[("compact", "Compact"), ("comfortable", "Comfortable"), ("detailed", "Detailed")], default="comfortable")
    dashboard_default_view = models.CharField(max_length=10, choices=[("patients", "Patients"), ("devices", "Devices"), ("alerts", "Alerts")], default="patients")
    dashboard_refresh_interval = models.IntegerField(default=30)  # In seconds

    # Notifications
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)
    push_notifications = models.BooleanField(default=True)

    do_not_disturb_enabled = models.BooleanField(default=False)
    do_not_disturb_start = models.TimeField(null=True, blank=True)
    do_not_disturb_end = models.TimeField(null=True, blank=True)
    exclude_emergency_alerts = models.BooleanField(default=True)

    # Accessibility
    high_contrast = models.BooleanField(default=False)
    large_text = models.BooleanField(default=False)
    reduce_motion = models.BooleanField(default=False)
    screen_reader = models.BooleanField(default=False)

    # Privacy
    share_analytics = models.BooleanField(default=True)
    share_location = models.BooleanField(default=False)
    activity_tracking = models.BooleanField(default=True)

    def __str__(self):
        return f"Preferences for {self.user.username}"
