import numpy as np
import pandas as pd
from PIL import Image
import io
from django.apps import apps

import tensorflow as tf
import keras
from keras.applications.mobilenet_v2 import preprocess_input


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

    return {'disease': predicted_class, 'confidence': round(confidence, 4)}


def recommend_crop(data: dict):
    """Preprocesses input data and returns crop recommendations."""
    model = get_artifact('crop_model')
    scaler = get_artifact('crop_scaler')
    encoder = get_artifact('crop_encoder')
    if not all([model, scaler, encoder]):
        raise RuntimeError("Crop model artifacts are not loaded.")

    # Convert data to DataFrame to ensure column order
    df = pd.DataFrame([data])
    scaled_df = scaler.transform(df)

    prediction = model.predict(scaled_df)
    predicted_crop = encoder.inverse_transform(prediction)[0]

    return {'recommended_crop': predicted_crop}


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