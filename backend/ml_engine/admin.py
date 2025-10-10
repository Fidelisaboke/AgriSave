from django.contrib import admin

from .models import (
    DiseaseDetector,
    CropRecommender,
    ClimateForecaster,
)


@admin.register(DiseaseDetector)
class DiseaseDetectionModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'model_file', 'created_at', 'updated_at')
    search_fields = ('name', 'version')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(CropRecommender)
class CropRecommendationModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'model_file', 'created_at', 'updated_at')
    search_fields = ('name', 'version')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)


@admin.register(ClimateForecaster)
class ClimateForecastingModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'model_file', 'created_at', 'updated_at')
    search_fields = ('name', 'version')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
