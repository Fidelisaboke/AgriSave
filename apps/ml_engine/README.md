# ML Engine

This app handles all machine learning operations for AgriSave.

## Current Status

- Models for disease detection and crop recommendation are implemented and integrated.
- Endpoints for disease detection and crop recommendation are functional.
- Climate forecasting model training has been implemented but not integrated to the API endpoint.
- The climate forecasting endpoint returns mock data. A mechanism for fetching real historical weather data needs to be 
implemented.

## Endpoints

1. **POST /api/ml/predict-disease/** - Disease detection from leaf images
2. **POST /api/ml/recommend-crop/** - Crop recommendations based on conditions
3. **POST /api/ml/climate-forecast/** - Climate forecasting
4. **GET /api/ml/status/** - ML service health check

## Day 3 Implementation Plan

### Crop Disease Detection
- Model: MobileNetV2 fine-tuned on PlantVillage dataset
- Input: Leaf images (224x224)
- Output: Disease name, confidence score, treatment recommendation

### Crop Recommendation
- Model: Random Forest Classifier
- Input: Soil type, rainfall, temperature, pH level
- Output: Top 3 recommended crops with suitability scores

### Climate Forecasting
- Model: LSTM
- Input: Location, historical weather data
- Output: 7-30 day forecast with temperature, rainfall, humidity

## Model Storage

Models will be stored in `media/models/` directory:
- `disease_detector/best_disease_detector.keras` - MobileNetV2 fine-tuned for crop disease detection
- `crop_recommendation/crop_recommender.pkl` - Random Forest for crop recommendations
- `climate_forecasting/best_climate_forecaster.keras` - LSTM for climate prediction
