from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlertViewSet, NotificationChannelViewSet, AlertRuleViewSet

router = DefaultRouter()
router.register("alerts", AlertViewSet)
router.register("notification-channels", NotificationChannelViewSet)
router.register("alert-rules", AlertRuleViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
