from django.db import models
from django.contrib.auth import get_user_model
import uuid
from django.db.models import Q

User = get_user_model()

class Appointment(models.Model):
    APPOINTMENT_TYPES = [("Virtual", "Virtual"), ("In-Person", "In-Person")]
    STATUS_CHOICES = [
        ("Scheduled", "Scheduled"),
        ("Confirmed", "Confirmed"),
        ("Completed", "Completed"),
        ("Cancelled", "Cancelled"),
        ("No-Show", "No-Show"),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointments",limit_choices_to={'role': 'patient'})
    provider = models.ForeignKey(User, on_delete=models.CASCADE, related_name="provider_appointments",limit_choices_to={'role': 'caregiver'})
    type = models.CharField(max_length=20, choices=APPOINTMENT_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Scheduled")
    date = models.DateField()
    time = models.TimeField()
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    purpose = models.TextField()
    notes = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    meeting_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.type} - {self.patient} with {self.provider} on {self.date} at {self.time}"
    class meta:
        ordering = ['date', 'time']


class Reminder(models.Model):
    REMINDER_TYPES = [("Email", "Email"), ("SMS", "SMS"), ("Push", "Push")]

    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name="reminders")
    type = models.CharField(max_length=10, choices=REMINDER_TYPES)
    scheduled_for = models.DateTimeField()
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type} reminder for {self.appointment}"

    class meta:
        ordering = ['scheduled_for']


class Schedule(models.Model):
    ROLE_CHOICES = [("provider", "Provider"), ("patient", "Patient")]
    user = models.OneToOneField(
        User, 
        on_delete=models.CASCADE, 
        related_name="schedule", 
        limit_choices_to=Q(role='patient') | Q(role='caregiver'))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    availability = models.JSONField(default=list, blank=True, null=True)
    breaks = models.JSONField(default=list, blank=True, null=True)

    def __str__(self):
        return f"Schedule for {self.user}"

    class meta:
        ordering = ['user']
    
    def save(self, *args, **kwargs):
        """Ensure the role is set to 'provider' for caregivers and 'patient' for patients."""
        if self.user.role == "caregiver":
            self.role = "provider"
        elif self.user.role == "patient":
            self.role = "patient"
        else:
            raise ValueError("Invalid role")
            
        super().save(*args, **kwargs)


class AppointmentRequest(models.Model):
    URGENCY_CHOICES = [("Normal", "Normal"), ("Urgent", "Urgent")]

    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="appointment_requests")
    preferred_dates = models.JSONField()
    type = models.CharField(max_length=20, choices=Appointment.APPOINTMENT_TYPES)
    purpose = models.TextField()
    notes = models.TextField(blank=True, null=True)
    urgency = models.CharField(max_length=10, choices=URGENCY_CHOICES)

    def __str__(self):
        return f"Request from {self.patient} - {self.urgency}"
    class meta: 
        ordering = ['urgency']
