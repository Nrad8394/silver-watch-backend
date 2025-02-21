from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.timezone import now, timedelta
from .models import Device, DeviceMaintenance, DeviceReading


@receiver(pre_save, sender=Device)
def check_device_status(sender, instance, **kwargs):
    """
    Alert when a device goes Offline or Critical.
    """
    if instance.pk:
        previous = Device.objects.get(pk=instance.pk)
        if previous.status != instance.status:
            if instance.status in ["Offline", "Critical"]:
                print(f"⚠️ Alert: Device {instance.id} is now {instance.status}")


@receiver(post_save, sender=DeviceMaintenance)
def schedule_next_maintenance(sender, instance, created, **kwargs):
    """
    Auto-schedule next maintenance when one is completed.
    """
    if created and instance.status == "Completed":
        if instance.type == "Calibration":
            next_date = now() + timedelta(days=90)  # Schedule in 3 months
        elif instance.type == "Battery Replacement":
            next_date = now() + timedelta(days=180)  # Schedule in 6 months
        elif instance.type == "Firmware Update":
            next_date = now() + timedelta(days=365)  # Schedule in 1 year
        else:
            next_date = now() + timedelta(days=120)  # Default: 4 months

        DeviceMaintenance.objects.create(
            device=instance.device,
            type=instance.type,
            status="Scheduled",
            scheduled_for=next_date
        )
        print(f"✅ Next {instance.type} scheduled for {instance.device} on {next_date}")


@receiver(pre_save, sender=DeviceReading)
def validate_device_reading(sender, instance, **kwargs):
    """
    Validate readings to prevent extreme values.
    """
    if instance.value < 0:
        raise ValueError("⚠️ Error: Sensor values cannot be negative!")
    if instance.type == "Heart Rate" and instance.value > 220:
        raise ValueError("⚠️ Error: Heart rate readings above 220 are not valid!")
    if instance.type == "Temperature" and (instance.value < 30 or instance.value > 45):
        raise ValueError("⚠️ Error: Temperature readings must be between 30-45°C!")


@receiver(post_save, sender=DeviceReading)
def log_critical_readings(sender, instance, created, **kwargs):
    """
    Log critical readings for review.
    """
    if created:
        if instance.type == "Heart Rate" and instance.value > 180:
            print(f"⚠️ Alert: High Heart Rate detected ({instance.value} bpm) for Device {instance.device.id}")
        elif instance.type == "Blood Pressure" and instance.value > 180:
            print(f"⚠️ Alert: High Blood Pressure detected ({instance.value} mmHg) for Device {instance.device.id}")
