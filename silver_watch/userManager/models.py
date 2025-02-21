from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from shortuuid.django_fields import ShortUUIDField
from datetime import datetime
import shortuuid
from phonenumber_field.modelfields import PhoneNumberField
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('caregiver', 'Caregiver'),
        ('technician', 'Technician'),
        ('patient', 'Patient'),
    ]
    
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    # ID with dynamically set year prefix
    id = models.CharField(
        max_length=20, primary_key=True, unique=True, editable=False
    )

    status = models.CharField(
        max_length=10, choices=[('Active', 'Active'), ('Inactive', 'Inactive')], default='Active'
    )
    last_active = models.DateTimeField(null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    phone_number = PhoneNumberField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def save(self, *args, **kwargs):
        """Ensure ID is generated dynamically with the current year as a prefix."""
        if not self.id:
            year_prefix = str(datetime.now().year)
            unique_part = shortuuid.ShortUUID(alphabet="1234567890").random(length=10)
            self.id = f"{year_prefix}{unique_part}"  
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email}"

    class Meta:
        ordering = ['-last_login', 'last_name', 'first_name']

class NotificationPreferences(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='notification_preferences')
    emergency_alerts = models.BooleanField(default=True)
    system_updates = models.BooleanField(default=True)
    daily_reports = models.BooleanField(default=True)
    team_messages = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)

    def __str__(self):
        return f"Notification Preferences for {self.user.email}"

    class Meta:
        ordering = ['user']
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    department = models.CharField(max_length=255, null=True, blank=True)
    specialization = models.CharField(max_length=255, null=True, blank=True)
    license_number = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"Profile of {self.user.email}"
    class Meta:
        ordering = ['-user__last_login','user__last_name', 'user__first_name']

class EmergencyContact(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=255)
    relationship = models.CharField(max_length=50)
    phone_number = PhoneNumberField()

    def __str__(self):
        return f"{self.name} ({self.relationship})"
    class Meta:
        ordering = ['user_profile']