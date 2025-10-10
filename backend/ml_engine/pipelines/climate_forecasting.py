"""
This module implements the training pipeline for a climate forecasting model using LSTM.
"""

import json
import logging
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from django.conf import settings
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.layers import Dense, Dropout, LSTM, Input
from keras.models import Sequential
from sklearn.preprocessing import MinMaxScaler

from ..models import ClimateForecaster

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def create_sequences(data, seq_length=14):
    """
    Creates sequences of data for time series forecasting.
    """
    sequences, targets = [], []
    for i in range(len(data) - seq_length):
        sequences.append(data[i:i + seq_length])
        targets.append(data[i + seq_length])
    return np.array(sequences), np.array(targets)


def run_climate_forecasting_training():
    """
    Orchestrates the training process for the climate forecasting model.
    """
    model_save_dir = Path(settings.ML_MODELS_DIR) / "climate_forecasting/"
    model_save_dir.mkdir(parents=True, exist_ok=True)

    # Load climate_forecasting dataset
    df = pd.read_csv(Path(settings.DATASETS_DIR) / "raw/nairobi_weather_data.csv")
    logging.info(f"Loaded dataset with {len(df)} records.")

    # Preprocess data
    # Set datetime as index and handle missing values
    df['datetime'] = pd.to_datetime(df['datetime'])
    df.set_index('datetime', inplace=True)
    df.sort_index(inplace=True)
    df.ffill(inplace=True)

    # Set feature columns
    feature_cols = ['temp', 'humidity', 'precip', 'windspeed', 'cloudcover']
    with open(model_save_dir / "feature_columns.json", 'w') as f:
        json.dump(feature_cols, f)
    logging.info(f"[SUCCESS] Saved feature columns to {model_save_dir / 'feature_columns.json'}")
    df_features = df[feature_cols]

    # Feature scaling
    scaler = MinMaxScaler()
    scaled_data = scaler.fit_transform(df_features)

    # Save the weather scaler
    joblib.dump(scaler, model_save_dir / "weather_scaler.pkl")
    logging.info(f"[SUCCESS] Saved weather scaler to {model_save_dir / 'weather_scaler.pkl'}")

    # Create sequences
    X, y = create_sequences(scaled_data, seq_length=14)
    logging.info(f"Created {len(X)} sequences for training.")

    # Split into training and testing sets
    split_index = int(0.8 * len(X))
    X_train, X_test = X[:split_index], X[split_index:]
    y_train, y_test = y[:split_index], y[split_index:]
    logging.info(f"Data split: {len(X_train)} training samples, {len(X_test)} testing samples.")

    # Build the LSTM model
    model = Sequential([
        Input(shape=(X_train.shape[1], X_train.shape[2])),
        LSTM(64, return_sequences=True),
        Dropout(0.2),
        LSTM(32),
        Dropout(0.2),
        Dense(len(feature_cols)),
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='mse')
    model.summary()

    # Save best model during training
    checkpoint_path = model_save_dir / "best_climate_forecaster.keras"
    checkpoint = ModelCheckpoint(str(checkpoint_path), monitor='val_loss', save_best_only=True)
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

    # Train the model
    model.fit(
        X_train, y_train,
        validation_split=0.1,
        epochs=30,
        batch_size=32,
        callbacks=[checkpoint, early_stopping]
    )

    # Evaluate the model
    loss = model.evaluate(X_test, y_test)
    logging.info(f"Test Loss: {loss:.4f}")

    # Make predictions
    y_pred_scaled = model.predict(X_test)

    # Inverse transform the predictions for all features
    y_pred = scaler.inverse_transform(y_pred_scaled)

    # Inverse transform the true values for all features
    y_true = scaler.inverse_transform(y_test)

    # Extract the 'temp' column for RMSE calculation
    y_pred_temp = y_pred[:, 0]
    y_true_temp = y_true[:, 0]

    # Calculate RMSE on the unscaled temperature predictions
    rmse = np.sqrt(np.mean((y_pred_temp - y_true_temp) ** 2))
    logging.info(f"Temperature Prediction RMSE: {rmse:.4f}")

    # Save the training job metadata to the database
    relative_path = checkpoint_path.relative_to(settings.MEDIA_ROOT)
    ClimateForecaster.objects.create(
        name="Climate Forecaster",
        version="1.0",
        model_file=str(relative_path),
        metrics={
            "test_loss": float(loss),
            "temperature_rmse": float(rmse)
        },
    )
    logging.info(f"[SUCCESS] Saved trained model metadata to the database.")
