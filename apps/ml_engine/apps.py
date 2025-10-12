import json
import logging
from pathlib import Path

import joblib
from django.apps import AppConfig
from django.conf import settings
from keras.models import load_model

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MlEngineConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.ml_engine'

    # In-memory ML model registry
    REGISTRY = {
        'disease_model': None, 'disease_classes': None,
        'crop_model': None, 'crop_scaler': None, 'crop_encoder': None,
        'climate_model': None, 'climate_scaler': None, 'climate_features': None,
    }

    def ready(self):
        # Temporarily disable ML model loading for deployment
        logging.info("ML model loading disabled for deployment")
        return

        # --- ML model loading code below is commented out ---
        # Disease detection artifacts
        # dd_path = Path(settings.ML_MODELS_DIR) / "disease_detection"
        # model_file = dd_path / "best_disease_detector.keras"
        # classes_file = dd_path / "class_names.json"

        # if model_file.exists() and classes_file.exists():
        #     logging.info("Disease Detection artifacts found, attempting to load model.")
        #     try:
        #         disease_model = load_model(model_file)
        #         with open(classes_file) as f:
        #             disease_classes = json.load(f)
        #         self.REGISTRY['disease_model'] = disease_model
        #         self.REGISTRY['disease_classes'] = disease_classes
        #         logging.info("[SUCCESS] Loaded Disease Detection model and classes.")
        #     except Exception as e:
        #         logging.error(f"Failed to load Disease Detection artifacts: {e}")

        # Crop Recommendation Artifacts
        # cr_path = Path(settings.ML_MODELS_DIR) / "crop_recommendation"
        # model_file = cr_path / "crop_recommender.pkl"
        # scaler_file = cr_path / "crop_scaler.pkl"
        # encoder_file = cr_path / "crop_label_encoder.pkl"

        # if model_file.exists() and scaler_file.exists() and encoder_file.exists():
        #     logging.info("Crop Recommendation artifacts found, attempting to load model.")
        #     try:
        #         self.REGISTRY['crop_model'] = joblib.load(model_file)
        #         self.REGISTRY['crop_scaler'] = joblib.load(scaler_file)
        #         self.REGISTRY['crop_encoder'] = joblib.load(encoder_file)
        #         logging.info("[SUCCESS] Loaded Crop Recommendation model and artifacts.")
        #     except Exception as e:
        #         logging.error(f"Failed to load Crop Recommendation model: {e}")

        # Climate Forecasting Artifacts
        # cf_path = Path(settings.ML_MODELS_DIR) / "climate_forecasting"
        # model_file = cf_path / "best_climate_forecaster.keras"
        # scaler_file = cf_path / "weather_scaler.pkl"
        # features_file = cf_path / "feature_columns.json"

        # if model_file.exists() and scaler_file.exists() and features_file.exists():
        #     logging.info("Climate Forecasting artifacts found, attempting to load model.")
        #     try:
        #         self.REGISTRY['climate_model'] = load_model(model_file)
        #         self.REGISTRY['climate_scaler'] = joblib.load(scaler_file)
        #         with open(features_file) as f:
        #             self.REGISTRY['climate_features'] = json.load(f)
        #         logging.info("[SUCCESS] Loaded Climate Forecasting model and artifacts.")
        #     except Exception as e:
        #         logging.error(f"Failed to load Climate Forecasting model: {e}")
