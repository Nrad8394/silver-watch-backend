from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import HealthReportViewSet, DeviceReportViewSet, AnalyticsDataViewSet

router = DefaultRouter()
router.register(r"health-reports", HealthReportViewSet)
router.register(r"device-reports", DeviceReportViewSet)
router.register(r"analytics-data", AnalyticsDataViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
