# ML Engine

This app handles all machine learning operations for AgriSave.

## Current Status (Day 2)

All endpoints return **mock data** for testing and development purposes.

## Endpoints

1. **POST /api/ml/predict-disease/** - Disease detection from leaf images
2. **POST /api/ml/recommend-crop/** - Crop recommendations based on conditions
3. **POST /api/ml/climate-forecast/** - Climate forecasting
4. **GET /api/ml/status/** - ML service health check

## Day 3 Implementation Plan

### Disease Detection
- Model: MobileNetV2 or ResNet50 fine-tuned on PlantVillage dataset
- Input: Leaf images (224x224)
- Output: Disease name, confidence score, treatment recommendation

### Crop Recommendation
- Model: Random Forest or XGBoost
- Input: Soil type, rainfall, temperature, pH level
- Output: Top 3 recommended crops with suitability scores

### Climate Forecasting
- Model: LSTM or Prophet
- Input: Location, historical weather data
- Output: 7-30 day forecast with temperature, rainfall, humidity

## Model Storage

Models will be stored in `ml_engine/models/` directory:
- `disease_detector.h5` - CNN for disease detection
- `crop_recommender.pkl` - Random Forest for crop recommendations
- `climate_forecaster.h5` - LSTM for climate prediction

## Dependencies (Day 3)

Additional packages needed: