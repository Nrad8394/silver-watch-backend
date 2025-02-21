from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VitalSignsViewSet, HealthMetricsViewSet, MedicalHistoryViewSet, HealthTrendViewSet

router = DefaultRouter()
router.register("vital-signs", VitalSignsViewSet)
router.register("health-metrics", HealthMetricsViewSet)
router.register("medical-history", MedicalHistoryViewSet)
router.register("health-trends", HealthTrendViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
