from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import CustomUser, UserProfile, NotificationPreferences, EmergencyContact

class UserProfileInline(admin.StackedInline):
    """
    Inline admin for displaying user profile details within the User admin panel.
    """
    model = UserProfile
    can_delete = False
    verbose_name_plural = "User Profile"
    fk_name = "user"
    extra = 0

class NotificationPreferencesInline(admin.StackedInline):
    """
    Inline admin for displaying notification preferences within the User admin panel.
    """
    model = NotificationPreferences
    can_delete = False
    verbose_name_plural = "Notification Preferences"
    fk_name = "user"
    extra = 0

@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    """
    Custom admin panel for managing users.
    """
    list_display = ('id', 'email', 'first_name', 'last_name', 'role', 'status', 'last_login')
    list_filter = ('role', 'status', 'is_staff', 'is_superuser', 'last_active')
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    ordering = ('-last_login',)
    readonly_fields = ('id', 'last_login')

    fieldsets = (
        ("User Details", {'fields': ('email', 'first_name', 'last_name', 'password')}),
        ("Role & Status", {'fields': ('role', 'status', 'phone_number', 'profile_image')}),
        ("Permissions", {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ("Timestamps", {'fields': ('last_login', 'last_active')}),
    )

    add_fieldsets = (
        ("Create User", {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'role', 'status')
        }),
    )

    inlines = [UserProfileInline, NotificationPreferencesInline]

    def get_inline_instances(self, request, obj=None):
        """
        Only show inlines when editing an existing user.
        """
        if not obj:
            return []
        return super().get_inline_instances(request, obj)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """
    Admin panel for managing user profiles.
    """
    list_display = ('id', 'user', 'department', 'specialization', 'license_number')
    search_fields = ('user__email', 'department', 'specialization')
    list_filter = ('department',)
    readonly_fields = ('id',)
    ordering = ('user__first_name',)

@admin.register(NotificationPreferences)
class NotificationPreferencesAdmin(admin.ModelAdmin):
    """
    Admin panel for managing user notification preferences.
    """
    list_display = ('user', 'email_notifications', 'sms_notifications', 'push_notifications')
    list_filter = ('email_notifications', 'sms_notifications', 'push_notifications')
    search_fields = ('user__email',)
    ordering = ('user__email',)

@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    """
    Admin panel for managing emergency contacts.
    """
    list_display = ('id', 'user_profile', 'name', 'relationship', 'phone_number')
    search_fields = ('user_profile__user__email', 'name', 'relationship', 'phone_number')
    list_filter = ('relationship',)
    ordering = ('user_profile__user__first_name',)
