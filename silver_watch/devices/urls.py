from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet, DeviceSettingsViewSet, DeviceMaintenanceViewSet, DeviceReadingViewSet

router = DefaultRouter()
router.register(r"devices", DeviceViewSet, basename="device")
router.register(r"settings", DeviceSettingsViewSet, basename="device-settings")
router.register(r"maintenance", DeviceMaintenanceViewSet, basename="device-maintenance")
router.register(r"readings", DeviceReadingViewSet, basename="device-readings")

urlpatterns = [
    path("", include(router.urls)),
]
