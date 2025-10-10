from rest_framework import serializers

from .models import (
    DiseaseDetector,
    CropRecommender,
    ClimateForecaster,
)


class DiseasePredictionSerializer(serializers.Serializer):
    """Serializer for disease prediction input"""
    image = serializers.ImageField(required=True)


class CropRecommendationSerializer(serializers.Serializer):
    """Serializer for crop recommendation input"""
    N = serializers.FloatField(required=True, min_value=0.0)
    P = serializers.FloatField(required=True, min_value=0.0)
    K = serializers.FloatField(required=True, min_value=0.0)
    temperature = serializers.FloatField(required=True)
    humidity = serializers.FloatField(required=True, min_value=0.0, max_value=100.0)
    ph = serializers.FloatField(required=True, min_value=0.0, max_value=14.0)
    rainfall = serializers.FloatField(required=True, min_value=0.0)


class ClimateForecastSerializer(serializers.Serializer):
    """Serializer for climate forecast input"""
    location = serializers.CharField(max_length=200, required=True)
    days = serializers.IntegerField(default=7, min_value=1, max_value=30)


class BaseMLModelSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'name', 'version', 'model_file', 'full_path', 'created_at', 'updated_at']
        read_only_fields = ['id', 'full_path', 'created_at']


class DiseaseDetectorSerializer(BaseMLModelSerializer):
    class Meta(BaseMLModelSerializer.Meta):
        model = DiseaseDetector


class CropRecommenderSerializer(BaseMLModelSerializer):
    class Meta(BaseMLModelSerializer.Meta):
        model = CropRecommender


class ClimateForecasterSerializer(BaseMLModelSerializer):
    class Meta(BaseMLModelSerializer.Meta):
        model = ClimateForecaster
