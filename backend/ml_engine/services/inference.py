import numpy as np
import pandas as pd
from PIL import Image
import io
import requests
from django.apps import apps

import tensorflow as tf
import keras
from keras.applications.mobilenet_v2 import preprocess_input

from ..utils import is_plant_healthy, calculate_severity, get_recommendation_for_class


def get_artifact(name):
    """Helper to get a loaded artifact from the registry."""
    return apps.get_app_config('ml_engine').REGISTRY.get(name)


def predict_disease(image_file):
    """Preprocesses an image and returns disease prediction."""
    model = get_artifact('disease_model')
    class_names = get_artifact('disease_classes')
    if not model or not class_names:
        raise RuntimeError("Disease model is not loaded.")

    # Preprocess image
    image_bytes = image_file.read()
    image = tf.image.decode_image(image_bytes, channels=3)
    image = tf.image.resize(image, [224, 224])
    img_array = keras.preprocessing.image.img_to_array(image)
    img_batch = np.expand_dims(img_array, axis=0)
    img_preprocessed = preprocess_input(np.copy(img_batch))

    # Get prediction
    prediction = model.predict(img_preprocessed)
    confidence = float(np.max(prediction[0]))
    predicted_class = class_names[np.argmax(prediction[0])]

    # Get predicted class name
    predicted_class_name = predicted_class.replace('___', ' ').replace('_', ' ')

    # Predictions result dict
    predictions_result = {
        'predicted_class': predicted_class_name,
        'confidence': round(confidence, 4),
        'severity': 'Low',
        'recommended_actions': None
    }

    # If healthy, return early
    if is_plant_healthy(predicted_class):
        return predictions_result
    
    # Set severity for non-healthy class
    predictions_result['severity'] = calculate_severity(confidence)

    # Get recommendations for non-healthy class
    predictions_result['recommended_actions'] = get_recommendation_for_class(predicted_class)

    return predictions_result


def recommend_crops(data: dict, top_n: int = 3):
    """Preprocesses input data and returns crop recommendations."""
    model = get_artifact('crop_model')
    scaler = get_artifact('crop_scaler')
    encoder = get_artifact('crop_encoder')
    if not all([model, scaler, encoder]):
        raise RuntimeError("Crop model artifacts are not loaded.")

    # Convert data to DataFrame to ensure column order
    df = pd.DataFrame([data])
    scaled_df = scaler.transform(df)

    # Get probabilities of all classes
    prediction_proba = model.predict_proba(scaled_df)

    # Get probabilities for first prediction
    probabilities = prediction_proba[0]

    # Get indices of the top N classes
    top_n_indices = np.argsort(probabilities)[-top_n:]

    # Reverse to get indices in descending order
    top_n_indices = top_n_indices[::-1]

    # Get the corresponding class names and confidence scores
    top_crops = encoder.classes_[top_n_indices]
    top_confidences = probabilities[top_n_indices]

    # Format output
    recommendations = []
    for crop, confidence in zip(top_crops, top_confidences):
        recommendations.append({
            'crop': crop,
            'confidence': round(float(confidence), 4)
        })

    return {'recommendations': recommendations}

def forecast_climate(past_days_data: np.ndarray):
    """Takes a sequence of past weather data and forecasts the next day."""
    model = get_artifact('climate_model')
    scaler = get_artifact('climate_scaler')
    if not all([model, scaler]):
        raise RuntimeError("Climate model artifacts are not loaded.")

    # Data is already scaled and sequenced by the caller
    # Reshape for single prediction: (1, n_past, n_features)
    input_sequence = np.expand_dims(past_days_data, axis=0)

    prediction_scaled = model.predict(input_sequence)
    prediction_actual = scaler.inverse_transform(prediction_scaled)

    # Return the forecast in a structured way
    feature_names = get_artifact('climate_features')
    forecast = dict(zip(feature_names, prediction_actual[0]))

    return {'forecast': forecast}
