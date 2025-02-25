from rest_framework import serializers
from django.contrib.auth.models import Group, Permission
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.exceptions import InvalidToken
from django.core.exceptions import ObjectDoesNotExist
from django.db.utils import IntegrityError
from .models import CustomUser, NotificationPreferences, UserProfile, EmergencyContact

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    Custom Token Refresh to handle cases where the user no longer exists.
    """
    def validate(self, attrs):
        try:
            return super().validate(attrs)
        except ObjectDoesNotExist:
            raise InvalidToken("User no longer exists.")

class CustomRegisterSerializer(RegisterSerializer):
    """
    Custom Registration Serializer to handle role assignment and unique email validation.
    """
    role = serializers.ChoiceField(choices=CustomUser.ROLE_CHOICES, required=True)

    def save(self, request):
        try:
            user = super().save(request)
            user.role = self.validated_data.get('role')
            self.assign_user_group(user)
            return user
        except IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                raise ValidationError({"email": "A user with this email already exists."})
            raise ValidationError({"detail": "A database error occurred."})

    def assign_user_group(self, user):
        """
        Assigns users to appropriate Django groups based on their role.
        """
        role_group_map = {
            'admin': 'Admin',
            'caregiver': 'Caregiver',
            'technician': 'Technician',
            'patient': 'Patient',
        }
        group_name = role_group_map.get(user.role)
        if group_name:
            group, _ = Group.objects.get_or_create(name=group_name)
            user.groups.add(group)

        if user.role == 'admin':
            user.is_staff = True
            # user.is_superuser = True

        user.save()

class ResendEmailVerificationSerializer(serializers.Serializer):
    """
    Serializer for resending email verification.
    """
    email = serializers.EmailField()

    def validate_email(self, value):
        if not CustomUser.objects.filter(email=value).exists():
            raise ValidationError("No account found with this email.")
        return value

class UserProfileSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Nested read-only user data
    user_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=CustomUser.objects.all(), source='user')

    class Meta:
        model = UserProfile
        fields = ["id", "user_id", "user", "department", "specialization", "license_number"]

class NotificationPreferencesSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)  # Nested read-only user data
    user_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=CustomUser.objects.all(), source='user')
    class Meta:
        model = NotificationPreferences
        fields = "__all__"

class EmergencyContactSerializer(serializers.ModelSerializer):
    user_profile = serializers.PrimaryKeyRelatedField(read_only=True)
    user_profile_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=UserProfile.objects.all(), source='user_profile')

    class Meta:
        model = EmergencyContact
        fields = "__all__"

class CustomUserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model with role and profile details.
    """
    group_names = serializers.SerializerMethodField()
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
        }
        read_only_fields = ['id', 'email', 'group_names', 'profile']

    def get_group_names(self, obj):
        return obj.groups.values_list('name', flat=True)

    def update(self, instance, validated_data):
        """
        Ensure only authorized fields can be updated.
        """
        user = self.context.get('request').user

        if not user.is_superuser:
            restricted_fields = ['is_staff', 'is_superuser', 'groups', 'role']
            for field in restricted_fields:
                validated_data.pop(field, None)

        return super().update(instance, validated_data)

class GroupSerializer(serializers.ModelSerializer):
    """
    Serializer for Django Group model.
    """
    permissions = serializers.PrimaryKeyRelatedField(queryset=Permission.objects.all(), many=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'permissions']

class PermissionSerializer(serializers.ModelSerializer):
    """
    Serializer for Permissions, including application and feature names.
    """
    app = serializers.SerializerMethodField()
    feature = serializers.CharField(source='name')
    permission = serializers.CharField(source='codename')

    class Meta:
        model = Permission
        fields = ['id', 'app', 'feature', 'permission']

    def get_app(self, obj):
        return obj.content_type.app_label

class UserTypePermissionSerializer(serializers.ModelSerializer):
    """
    Serializer to show user groups and permissions.
    """
    groups = GroupSerializer(many=True)

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'groups']
