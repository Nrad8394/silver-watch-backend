from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from .models import Device, DeviceSettings, DeviceMaintenance, DeviceReading
from .serializers import (
    DeviceSerializer,
    DeviceSettingsSerializer,
    DeviceMaintenanceSerializer,
    DeviceReadingSerializer
)
from .filters import DeviceFilter, DeviceMaintenanceFilter, DeviceReadingFilter
from .mixins import ReadOnlyViewSet


class DeviceViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing devices.
    - Anyone can retrieve a device.
    - Only authenticated users can list, create, update, and delete devices.
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = DeviceFilter

    def get_permissions(self):
        if self.action == 'retrieve':
            return []  # No authentication required for retrieving a device
        return [permissions.IsAuthenticated()]


class DeviceSettingsViewSet(viewsets.ModelViewSet):
    """
    Viewset for device settings management.
    """
    queryset = DeviceSettings.objects.all()
    serializer_class = DeviceSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]


class DeviceMaintenanceViewSet(viewsets.ModelViewSet):
    """
    Viewset for managing device maintenance records.
    """
    queryset = DeviceMaintenance.objects.all()
    serializer_class = DeviceMaintenanceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = DeviceMaintenanceFilter


class DeviceReadingViewSet(ReadOnlyViewSet):
    """
    Read-only viewset for device readings.
    """
    queryset = DeviceReading.objects.all().order_by("-timestamp")
    serializer_class = DeviceReadingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = DeviceReadingFilter
