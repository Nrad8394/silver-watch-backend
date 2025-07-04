# Generated by Django 5.1.6 on 2025-02-21 16:23

import django.db.models.deletion
import django.db.models.fields
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.UUIDField(default=django.db.models.fields.UUIDField, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('Heart Monitor', 'Heart Monitor'), ('Temperature Sensor', 'Temperature Sensor'), ('Motion Sensor', 'Motion Sensor'), ('Blood Pressure Monitor', 'Blood Pressure Monitor'), ('Wearable Device', 'Wearable Device')], max_length=50)),
                ('status', models.CharField(choices=[('Online', 'Online'), ('Offline', 'Offline'), ('Warning', 'Warning'), ('Critical', 'Critical')], max_length=20)),
                ('battery_level', models.FloatField()),
                ('signal_strength', models.FloatField()),
                ('last_maintenance', models.DateTimeField()),
                ('next_maintenance', models.DateTimeField()),
                ('location', models.CharField(max_length=255)),
                ('firmware_version', models.CharField(max_length=50)),
                ('firmware_last_update', models.DateTimeField()),
                ('firmware_available_update', models.CharField(blank=True, max_length=50, null=True)),
                ('last_calibrated', models.DateTimeField()),
                ('next_calibration', models.DateTimeField()),
                ('calibration_accuracy', models.FloatField()),
                ('calibration_status', models.CharField(choices=[('Calibrated', 'Calibrated'), ('Needs Calibration', 'Needs Calibration'), ('In Progress', 'In Progress')], max_length=20)),
                ('assigned_to', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceMaintenance',
            fields=[
                ('id', models.UUIDField(default=django.db.models.fields.UUIDField, editable=False, primary_key=True, serialize=False)),
                ('type', models.CharField(choices=[('Calibration', 'Calibration'), ('Battery Replacement', 'Battery Replacement'), ('Firmware Update', 'Firmware Update'), ('Hardware Check', 'Hardware Check')], max_length=50)),
                ('status', models.CharField(choices=[('Scheduled', 'Scheduled'), ('In Progress', 'In Progress'), ('Completed', 'Completed'), ('Failed', 'Failed')], max_length=20)),
                ('scheduled_for', models.DateTimeField()),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('notes', models.TextField(blank=True, null=True)),
                ('results', models.JSONField(blank=True, null=True)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='maintenance_records', to='devices.device')),
                ('technician', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DeviceReading',
            fields=[
                ('id', models.UUIDField(default=django.db.models.fields.UUIDField, editable=False, primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('reading_type', models.CharField(max_length=100)),
                ('value', models.FloatField()),
                ('unit', models.CharField(max_length=20)),
                ('device', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='readings', to='devices.device')),
            ],
        ),
        migrations.CreateModel(
            name='DeviceSettings',
            fields=[
                ('id', models.UUIDField(default=django.db.models.fields.UUIDField, editable=False, primary_key=True, serialize=False)),
                ('sensitivity', models.FloatField()),
                ('threshold', models.FloatField()),
                ('sample_rate', models.FloatField()),
                ('auto_calibration', models.BooleanField(default=False)),
                ('high_precision_mode', models.BooleanField(default=False)),
                ('error_compensation', models.BooleanField(default=False)),
                ('alert_thresholds', models.JSONField(default=dict)),
                ('device', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to='devices.device')),
            ],
        ),
    ]
