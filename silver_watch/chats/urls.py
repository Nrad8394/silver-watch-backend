from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ConversationViewSet, MessageViewSet, ContactViewSet

router = DefaultRouter()
router.register(r"conversations", ConversationViewSet)
router.register(r"messages", MessageViewSet)
router.register(r"contacts", ContactViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
