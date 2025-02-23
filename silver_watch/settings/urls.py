from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SystemSettingsViewSet, APIKeyViewSet, WebhookViewSet, UserPreferencesViewSet

router = DefaultRouter()
router.register(r"system-settings", SystemSettingsViewSet)
router.register(r"api-keys", APIKeyViewSet)
router.register(r"webhooks", WebhookViewSet)
router.register(r"user-preferences", UserPreferencesViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
