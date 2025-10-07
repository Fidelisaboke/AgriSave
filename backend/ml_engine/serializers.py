from rest_framework import serializers


class DiseasePredictionSerializer(serializers.Serializer):
    """Serializer for disease prediction input"""
    image = serializers.ImageField(required=True)


class CropRecommendationSerializer(serializers.Serializer):
    """Serializer for crop recommendation input"""
    soil_type = serializers.CharField(max_length=50, required=True)
    rainfall = serializers.FloatField(required=True)
    temperature = serializers.FloatField(required=True)
    ph_level = serializers.FloatField(required=False)
    location = serializers.CharField(max_length=200, required=False)


class ClimateForecastSerializer(serializers.Serializer):
    """Serializer for climate forecast input"""
    location = serializers.CharField(max_length=200, required=True)
    days = serializers.IntegerField(default=7, min_value=1, max_value=30)