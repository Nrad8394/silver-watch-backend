from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now
from .models import Appointment, Reminder
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=Appointment)
def create_reminders(sender, instance, created, **kwargs):
    if created:
        logger.info(f"Creating reminders for appointment: {instance}")
        Reminder.objects.create(appointment=instance, type="Email", scheduled_for=instance.date, sent=False)
