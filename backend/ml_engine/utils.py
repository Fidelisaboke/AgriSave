"""
Utility functions for ML Engine
These will be used when integrating real ML models
"""
import os
from pathlib import Path


def get_model_path(model_name):
    """Get the full path to a model file"""
    base_dir = Path(__file__).resolve().parent
    model_dir = base_dir / 'models'
    return model_dir / model_name


def load_disease_model():
    """
    Load the disease detection model
    To be implemented on Day 3
    """
    # model_path = get_model_path('disease_detector.h5')
    # model = load_model(model_path)
    # return model
    return None


def load_crop_recommendation_model():
    """
    Load the crop recommendation model
    To be implemented on Day 3
    """
    # model_path = get_model_path('crop_recommender.pkl')
    # model = joblib.load(model_path)
    # return model
    return None


def load_climate_model():
    """
    Load the climate forecasting model
    To be implemented on Day 3
    """
    # model_path = get_model_path('climate_forecaster.h5')
    # model = load_model(model_path)
    # return model
    return None


def preprocess_leaf_image(image):
    """
    Preprocess leaf image for disease detection
    To be implemented on Day 3
    """
    # from PIL import Image
    # import numpy as np
    # img = Image.open(image)
    # img = img.resize((224, 224))
    # img_array = np.array(img) / 255.0
    # return np.expand_dims(img_array, axis=0)
    return None


def format_prediction_result(prediction, confidence):
    """Format ML prediction results"""
    return {
        'prediction': prediction,
        'confidence': float(confidence),
        'reliable': confidence > 0.8
    }