"""
This module implements the training pipeline for a crop recommendation model using RandomForestClassifier.
"""

import logging
from pathlib import Path

import joblib
import pandas as pd
from django.conf import settings
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler

from ..models import CropRecommender

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def run_crop_recommendation_training():
    """
    Orchestrates the training process for the disease detection model.
    """
    model_save_dir = Path(settings.ML_MODELS_DIR) / "crop_recommendation/"
    model_save_dir.mkdir(parents=True, exist_ok=True)
    # Load crop_recommendations dataset
    df = pd.read_csv(Path(settings.DATASETS_DIR) / "raw/Crop_recommendations.csv")
    logging.info(f"Loaded dataset with {len(df)} records.")

    # Preprocess data
    X = df.drop('label', axis=1)
    y = df['label']

    # Scale numerical features
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled = pd.DataFrame(X_scaled, columns=X.columns)

    # Save the crop scaler
    joblib.dump(scaler, model_save_dir / "crop_scaler.pkl")
    logging.info(f"[SUCCESS] Saved crop scaler to {model_save_dir / 'crop_scaler.pkl'}")

    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)
    logging.info(f"Encoded labels: {list(label_encoder.classes_)}")

    # Save the label encoder
    joblib.dump(label_encoder, model_save_dir / "crop_label_encoder.pkl")
    logging.info(f"[SUCCESS] Saved label encoder to {model_save_dir / 'crop_label_encoder.pkl'}")

    # Split into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X_scaled, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
    )
    logging.info(f"Data split: {len(X_train)} training samples, {len(X_test)} testing samples.")

    # Train a RandomForestClassifier
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Print classification report
    y_pred = model.predict(X_test)
    report_str = classification_report(y_test, y_pred, target_names=label_encoder.classes_)
    report_dict = classification_report(y_test, y_pred, target_names=label_encoder.classes_, output_dict=True)
    logging.info(f"Crop Recommender Classification Report:\n {report_str}")

    # Save the trained model
    model_path = model_save_dir / 'crop_recommender.pkl'
    joblib.dump(model, model_path)
    logging.info(f"[SUCCESS] Saved trained model to {model_path}")

    # Save the training job metadata to the database
    relative_path = model_path.relative_to(settings.MEDIA_ROOT)
    CropRecommender.objects.create(
        name="Crop Recommender",
        version="1.0",
        model_file=str(relative_path),
        metrics=report_dict,
    )
    logging.info(f"[SUCCESS] Saved trained model metadata to the database.")
