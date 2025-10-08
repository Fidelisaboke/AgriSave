from django.contrib import admin
from .models import (
    DiseaseDetectionModel,
    CropRecommendationModel,
    ClimateForecastingModel,
)

@admin.register(DiseaseDetectionModel)
class DiseaseDetectionModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'model_file', 'created_at', 'updated_at')
    search_fields = ('name', 'version')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(CropRecommendationModel)
class CropRecommendationModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'model_file', 'created_at', 'updated_at')
    search_fields = ('name', 'version')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

@admin.register(ClimateForecastingModel)
class ClimateForecastingModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'version', 'model_file', 'created_at', 'updated_at')
    search_fields = ('name', 'version')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
