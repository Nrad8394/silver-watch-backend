from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import VitalSigns, HealthMetrics, MedicalHistory, HealthTrend
from .serializers import VitalSignsSerializer, HealthMetricsSerializer, MedicalHistorySerializer, HealthTrendSerializer

class VitalSignsViewSet(viewsets.ModelViewSet):
    queryset = VitalSigns.objects.all()
    serializer_class = VitalSignsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == "patient":
            return self.queryset.filter(patient=self.request.user)
        return self.queryset


class HealthMetricsViewSet(viewsets.ModelViewSet):
    queryset = HealthMetrics.objects.all()
    serializer_class = HealthMetricsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == "patient":
            return self.queryset.filter(patient=self.request.user)
        return self.queryset


class MedicalHistoryViewSet(viewsets.ModelViewSet):
    queryset = MedicalHistory.objects.all()
    serializer_class = MedicalHistorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == "patient":
            return self.queryset.filter(patient=self.request.user)
        return self.queryset


class HealthTrendViewSet(viewsets.ModelViewSet):
    queryset = HealthTrend.objects.all()
    serializer_class = HealthTrendSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if self.request.user.role == "patient":
            return self.queryset.filter(patient=self.request.user)
        return self.queryset
