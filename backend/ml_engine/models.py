"""
Django ORM models for storing metadata about
various machine learning models used in the application.
"""

import os

from django.conf import settings
from django.db import models


class BaseMLModel(models.Model):
    """Abstract base class for all ML models."""

    name = models.CharField(max_length=100)
    version = models.CharField(max_length=10)
    model_file = models.FileField(upload_to="ml_models/")
    metrics = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def full_path(self):
        return os.path.join(settings.MEDIA_ROOT, str(self.model_file))

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.name} (v{self.version})"


class DiseaseDetector(BaseMLModel):
    """Model for detecting plant diseases."""

    model_file = models.FileField(upload_to="ml_models/disease_detection/")

    class Meta:
        verbose_name = "Disease Detection Model"
        verbose_name_plural = "Disease Detection Models"


class CropRecommender(BaseMLModel):
    """Model for recommending crops based on soil and weather data."""

    model_file = models.FileField(upload_to="ml_models/crop_recommendation/")

    class Meta:
        verbose_name = "Crop Recommendation Model"
        verbose_name_plural = "Crop Recommendation Models"


class ClimateForecaster(BaseMLModel):
    """Model for forecasting climate conditions."""

    model_file = models.FileField(upload_to="ml_models/climate_forecasting/")

    class Meta:
        verbose_name = "Climate Forecasting Model"
        verbose_name_plural = "Climate Forecasting Models"
