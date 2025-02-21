import django_filters
from .models import Device, DeviceMaintenance, DeviceReading


class DeviceFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(field_name="type", lookup_expr="iexact")
    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")
    location = django_filters.CharFilter(field_name="location", lookup_expr="icontains")
    assigned_to = django_filters.CharFilter(field_name="assigned_to__username", lookup_expr="iexact")

    class Meta:
        model = Device
        fields = ["type", "status", "location", "assigned_to"]


class DeviceMaintenanceFilter(django_filters.FilterSet):
    type = django_filters.CharFilter(field_name="type", lookup_expr="iexact")
    status = django_filters.CharFilter(field_name="status", lookup_expr="iexact")
    technician = django_filters.CharFilter(field_name="technician__username", lookup_expr="iexact")
    scheduled_for = django_filters.DateFromToRangeFilter(field_name="scheduled_for")

    class Meta:
        model = DeviceMaintenance
        fields = ["type", "status", "technician", "scheduled_for"]


class DeviceReadingFilter(django_filters.FilterSet):
    device = django_filters.CharFilter(field_name="device__id", lookup_expr="iexact")
    reading_type = django_filters.CharFilter(field_name="reading_type", lookup_expr="iexact")
    timestamp = django_filters.DateFromToRangeFilter(field_name="timestamp")

    class Meta:
        model = DeviceReading
        fields = ["device", "reading_type", "timestamp"]
