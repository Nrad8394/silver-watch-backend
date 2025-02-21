import django_filters
from .models import CustomUser, NotificationPreferences, UserProfile, EmergencyContact


class UserFilter(django_filters.FilterSet):
    """
    Filters for CustomUser model.
    Allows filtering by role, status, and email.
    """
    role = django_filters.ChoiceFilter(choices=CustomUser.ROLE_CHOICES)
    status = django_filters.ChoiceFilter(choices=[('Active', 'Active'), ('Inactive', 'Inactive')])
    email = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = CustomUser
        fields = ['role', 'status', 'email']


class NotificationPreferencesFilter(django_filters.FilterSet):
    """
    Filters for NotificationPreferences model.
    Allows filtering by notification preferences.
    """
    emergency_alerts = django_filters.BooleanFilter()
    system_updates = django_filters.BooleanFilter()
    daily_reports = django_filters.BooleanFilter()
    team_messages = django_filters.BooleanFilter()
    email_notifications = django_filters.BooleanFilter()
    sms_notifications = django_filters.BooleanFilter()
    push_notifications = django_filters.BooleanFilter()

    class Meta:
        model = NotificationPreferences
        fields = [
            'emergency_alerts', 'system_updates', 'daily_reports',
            'team_messages', 'email_notifications', 'sms_notifications', 'push_notifications'
        ]


class UserProfileFilter(django_filters.FilterSet):
    """
    Filters for UserProfile model.
    Allows filtering by department, specialization, and license number.
    """
    department = django_filters.CharFilter(lookup_expr='icontains')
    specialization = django_filters.CharFilter(lookup_expr='icontains')
    license_number = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = UserProfile
        fields = ['department', 'specialization', 'license_number']


class EmergencyContactFilter(django_filters.FilterSet):
    """
    Filters for EmergencyContact model.
    Allows filtering by user profile, name, relationship, and phone number.
    """
    user_profile = django_filters.ModelChoiceFilter(queryset=UserProfile.objects.all())
    name = django_filters.CharFilter(lookup_expr='icontains')
    relationship = django_filters.CharFilter(lookup_expr='icontains')
    phone_number = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = EmergencyContact
        fields = ['user_profile', 'name', 'relationship', 'phone_number']
