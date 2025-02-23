from rest_framework import viewsets
from .models import HealthReport, DeviceReport, AnalyticsData
from .serializers import HealthReportSerializer, DeviceReportSerializer, AnalyticsDataSerializer

class HealthReportViewSet(viewsets.ModelViewSet):
    queryset = HealthReport.objects.all()
    serializer_class = HealthReportSerializer

class DeviceReportViewSet(viewsets.ModelViewSet):
    queryset = DeviceReport.objects.all()
    serializer_class = DeviceReportSerializer

class AnalyticsDataViewSet(viewsets.ModelViewSet):
    queryset = AnalyticsData.objects.all()
    serializer_class = AnalyticsDataSerializer
