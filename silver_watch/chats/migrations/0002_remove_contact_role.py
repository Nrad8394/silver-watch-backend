# Generated by Django 5.1.6 on 2025-02-23 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contact',
            name='role',
        ),
    ]
