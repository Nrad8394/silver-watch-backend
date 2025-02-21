from rest_framework import serializers
from .models import VitalSigns, HealthMetrics, MedicalHistory, HealthTrend

class VitalSignsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalSigns
        fields = "__all__"


class HealthMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthMetrics
        fields = "__all__"


class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = "__all__"


class HealthTrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthTrend
        fields = "__all__"
