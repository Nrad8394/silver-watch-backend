from rest_framework import serializers
from .models import Device, DeviceSettings, DeviceMaintenance, DeviceReading


class DeviceSerializer(serializers.ModelSerializer):
    assigned_to = serializers.StringRelatedField()  # Show username instead of ID

    class Meta:
        model = Device
        fields = "__all__"


class DeviceSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceSettings
        fields = "__all__"


class DeviceMaintenanceSerializer(serializers.ModelSerializer):
    technician = serializers.StringRelatedField()  # Show username instead of ID

    class Meta:
        model = DeviceMaintenance
        fields = "__all__"


class DeviceReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceReading
        fields = "__all__"
