from rest_framework import serializers
from .models import Device, DeviceSettings, DeviceMaintenance, DeviceReading


class DeviceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Device
        fields = "__all__"



class DeviceSettingsSerializer(serializers.ModelSerializer):
    device = serializers.PrimaryKeyRelatedField(queryset=Device.objects.all())
    
    class Meta:
        model = DeviceSettings
        fields = "__all__"


class DeviceMaintenanceSerializer(serializers.ModelSerializer):
    technician = serializers.StringRelatedField(read_only=True)  # Show username instead of ID
    
    class Meta:
        model = DeviceMaintenance
        fields = "__all__"


class DeviceReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceReading
        fields = "__all__"
