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
    Supports listing, retrieving, creating, updating, and deleting devices.
    """
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = DeviceFilter


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
