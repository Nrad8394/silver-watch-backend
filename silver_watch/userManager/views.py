from rest_framework import viewsets, permissions
from .models import CustomUser, UserProfile, NotificationPreferences, EmergencyContact
from .serializers import (
    CustomUserSerializer, 
    UserProfileSerializer, 
    NotificationPreferencesSerializer, 
    EmergencyContactSerializer
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .mixins import RoleBasedQuerysetMixin


# CustomUser Viewset (Manages Authentication & Core User Data)
class CustomUserViewSet(viewsets.ModelViewSet, RoleBasedQuerysetMixin):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ["email", "first_name", "last_name"]
    ordering_fields = ["last_active"]
    filterset_fields = ["role", "status"]

    def get_queryset(self):
        return self.get_filtered_queryset(CustomUser)


# User Profile Viewset (Manages Additional User Details)
class UserProfileViewSet(viewsets.ModelViewSet, RoleBasedQuerysetMixin):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["department", "specialization"]

    def get_queryset(self):
        return self.get_filtered_queryset(UserProfile)


# Notification Preferences Viewset
class NotificationPreferencesViewSet(viewsets.ModelViewSet, RoleBasedQuerysetMixin):
    queryset = NotificationPreferences.objects.all()
    serializer_class = NotificationPreferencesSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        return self.get_filtered_queryset(NotificationPreferences)


# Emergency Contact Viewset
class EmergencyContactViewSet(viewsets.ModelViewSet, RoleBasedQuerysetMixin):
    queryset = EmergencyContact.objects.all()
    serializer_class = EmergencyContactSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.DjangoModelPermissions]

    def get_queryset(self):
        return self.get_filtered_queryset(EmergencyContact)
