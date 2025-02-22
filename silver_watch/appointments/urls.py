from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AppointmentViewSet, ReminderViewSet, ScheduleViewSet, AppointmentRequestViewSet

router = DefaultRouter()
router.register(r"appointments", AppointmentViewSet)
router.register(r"reminders", ReminderViewSet)
router.register(r"schedules", ScheduleViewSet)
router.register(r"requests", AppointmentRequestViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
