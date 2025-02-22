import django_filters
from .models import Appointment

class AppointmentFilter(django_filters.FilterSet):
    patient = django_filters.CharFilter(field_name="patient__id", lookup_expr="exact")
    provider = django_filters.CharFilter(field_name="provider__id", lookup_expr="exact")
    status = django_filters.ChoiceFilter(choices=Appointment.STATUS_CHOICES)
    type = django_filters.ChoiceFilter(choices=Appointment.APPOINTMENT_TYPES)
    date = django_filters.DateFilter(field_name="date", lookup_expr="exact")
    date_range = django_filters.DateFromToRangeFilter(field_name="date")

    class Meta:
        model = Appointment
        fields = ["patient", "provider", "status", "type", "date", "date_range"]
