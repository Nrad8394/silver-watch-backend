from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Contact
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.utils.timezone import now
User = get_user_model()

@receiver(post_save, sender=User)
def create_contact_for_new_user(sender, instance, created, **kwargs):
    if created:
        Contact.objects.create(user=instance, name=instance.username)


@receiver(user_logged_in)
def update_status_online(sender, request, user, **kwargs):
    Contact.objects.filter(user=user).update(status=Contact.ONLINE, last_seen=now())

@receiver(user_logged_out)
def update_status_offline(sender, request, user, **kwargs):
    Contact.objects.filter(user=user).update(status=Contact.OFFLINE, last_seen=now())
