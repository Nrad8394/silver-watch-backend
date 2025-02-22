from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.timezone import now
from .models import Alert, NotificationChannel
from django.core.mail import send_mail
import logging

logger = logging.getLogger(__name__)


# 🚨 1. Auto-send notification when a new alert is created
@receiver(post_save, sender=Alert)
def send_alert_notification(sender, instance, created, **kwargs):
    if created:
        logger.info(f"New alert created: {instance.message}")

        # Get all notification channels for the target user (if applicable)
        channels = NotificationChannel.objects.filter(user_id=instance.target_id, enabled=True, verified=True)

        for channel in channels:
            if channel.type == "Email":
                send_mail(
                    subject=f"[{instance.priority}] {instance.type} Alert",
                    message=f"Alert: {instance.message}\n\nCategory: {instance.category}\nPriority: {instance.priority}",
                    from_email="alerts@yourapp.com",
                    recipient_list=[channel.target],
                )
            elif channel.type == "SMS":
                # You can integrate an SMS API here
                logger.info(f"Sending SMS alert to {channel.target}: {instance.message}")
            elif channel.type == "Push":
                # Push notification logic (e.g., Firebase)
                logger.info(f"Sending push notification: {instance.message}")


# ✅ 2. Log when an alert status changes (e.g., Active → Resolved)
@receiver(post_save, sender=Alert)
def log_alert_status_change(sender, instance, **kwargs):
    if instance.pk:  # Check if it's an update
        previous = Alert.objects.get(pk=instance.pk)
        if previous.status != instance.status:
            logger.info(f"Alert status changed: {previous.status} → {instance.status}")
            if instance.status == "Resolved":
                instance.resolution_at = now()


# 🚀 3. Auto-escalate high-priority alerts if not resolved in time
@receiver(post_save, sender=Alert)
def escalate_unresolved_alerts(sender, instance, **kwargs):
    if instance.status == "Active" and instance.priority == "High":
        logger.warning(f"High-priority alert needs attention: {instance.message}")
        # Escalation logic (e.g., notify admins)


# 📢 4. Notify admins if an alert rule is violated
@receiver(post_save, sender=Alert)
def check_alert_rules(sender, instance, **kwargs):
    from .models import AlertRule

    rules = AlertRule.objects.filter(enabled=True)
    for rule in rules:
        if instance.category == rule.metric and eval(f"{instance.priority} {rule.operator} {rule.value}"):
            logger.info(f"Alert rule triggered: {rule.name}")
            # Trigger rule actions (e.g., send notifications, escalate)
