# AgriSave ML Engine: Model Documentation

This document provides technical details on the architecture, training process, and usage of the machine learning models powering the AgriSave application.

---

## 1. Crop Disease Detection Model

### Model Overview

* **Purpose**: To identify the specific disease of a plant from an uploaded image of its leaf.
* **Type**: Image Classification
* **ID**: `disease_detector`

### Architecture

This model utilizes **transfer learning** for high accuracy and efficient training.

* **Base Model**: `MobileNetV2` pre-trained on the ImageNet dataset. The convolutional base is frozen (`trainable = False`) to retain its powerful feature extraction capabilities.
* **Input Shape**: `(224, 224, 3)` - RGB images resized to 224x224 pixels.
* **Custom Head**:
    1.  **Data Augmentation**: `RandomFlip`, `RandomRotation`, and `RandomZoom` layers are applied to the input images to create variations and prevent overfitting.
    2.  `GlobalAveragePooling2D`: Flattens the feature maps from the base model into a single vector.
    3.  `Dropout(0.2)`: A regularization layer to further prevent overfitting.
    4.  `Dense(15, activation='softmax')`: The final output layer, producing a probability score for each of the 15 possible disease classes.

### Training Process

* **Dataset**: PlantVillage image dataset, sourced from Kaggle.
* **Data Pipeline**: An efficient `tf.data.Dataset` pipeline is used to load and preprocess images in batches from their file paths, which is highly memory-efficient.
* **Labels**: The 15 class labels are one-hot encoded using `sklearn.preprocessing.LabelBinarizer`.
* **Data Split**: 80% for training, 20% for validation. The split is stratified to maintain the original class distribution in both sets.
* **Compilation**:
    * **Optimizer**: `adam`
    * **Loss Function**: `categorical_crossentropy`
    * **Metrics**: `accuracy`
* **Callbacks**:
    * `EarlyStopping`: Monitors `val_accuracy` and stops training after 3 epochs with no improvement.
    * `ModelCheckpoint`: Saves only the best performing model based on `val_accuracy`.

### Saved Artifacts

* `best_disease_detector.keras`: The trained Keras model file.
* `class_names.json`: A JSON list of the 15 class names, in the order the model was trained on.

### Usage (Inference)

* **Input**: A single image file of a plant leaf.
* **Preprocessing**: The image must be resized to `224x224` and pixel values normalized to the `[0, 1]` range.
* **Output**: A dictionary containing the predicted disease name and the model's confidence score.

---

## 2. Crop Recommendation Model

### Model Overview

* **Purpose**: To recommend the most suitable crop to grow based on soil composition and environmental data.
* **Type**: Tabular Classification
* **ID**: `crop_recommender`

### Architecture

* **Model**: `sklearn.ensemble.RandomForestClassifier`
* **Configuration**:
    * `n_estimators=100`: The model is an ensemble of 100 decision trees.
    * `random_state=42`: Ensures reproducibility.

### Training Process

* **Dataset**: Crop Recommendation dataset, sourced from Kaggle.
* **Features**: `N`, `P`, `K`, `temperature`, `humidity`, `ph`, `rainfall`.
* **Preprocessing**:
    1.  **Scaling**: All numerical features are scaled to a `[0, 1]` range using `MinMaxScaler`.
    2.  **Encoding**: The categorical `label` (crop name) is converted to integer representation using `LabelEncoder`.
* **Data Split**: 80% for training, 20% for testing, stratified by the encoded labels.
* **Evaluation**: Model performance is measured using a `classification_report`, which includes precision, recall, and F1-score for each crop.

### Saved Artifacts

* `crop_recommender.pkl`: The trained scikit-learn model object.
* `crop_scaler.pkl`: The fitted `MinMaxScaler` instance, essential for preprocessing new data at inference time.
* `crop_label_encoder.pkl`: The fitted `LabelEncoder` instance, required to convert the model's numeric output back to a crop name.

### Usage (Inference)

* **Input**: A dictionary containing the 7 required features (e.g., `{'N': 90, 'P': 42, ...}`).
* **Preprocessing**: The input data must be scaled using the saved `crop_scaler.pkl`.
* **Output**: The name of the single best crop to plant (e.g., `'rice'`).

---

## 3. Climate Forecasting Model

### Model Overview

* **Purpose**: To forecast a multi-variate weather forecast for the next day based on a sequence of historical weather data.
* **Type**: Time-Series Forecasting
* **ID**: `climate_forecaster`

### Architecture

The model is a stacked Long Short-Term Memory (LSTM) network designed to capture temporal patterns in the weather data.

* **Input Shape**: `(14, 5)` - A sequence of data from the last 14 days, with 5 features per day.
* **Layers**:
    1.  `Input(shape=(14, 5))`: Defines the expected input shape.
    2.  `LSTM(64, return_sequences=True)`: The first LSTM layer processes the sequence and outputs a full sequence to the next layer.
    3.  `Dropout(0.2)`: Regularization layer.
    4.  `LSTM(32)`: The second LSTM layer processes the sequence and outputs a single vector representing the learned patterns.
    5.  `Dropout(0.2)`: Regularization layer.
    6.  `Dense(5)`: The final output layer, which predicts the 5 feature values for the next day.

### Training Process

* **Dataset**: Nairobi Weather Data, sourced from Kaggle.
* **Features**: `temp`, `humidity`, `precip`, `windspeed`, `cloudcover`.
* **Preprocessing**:
    1.  **Scaling**: The 5 features are scaled to a `[0, 1]` range using `MinMaxScaler`.
    2.  **Sequencing**: The time-series data is transformed into overlapping sequences. Each input sample (`X`) consists of 14 consecutive days of data, and its corresponding target (`y`) is the data for the 15th day.
* **Data Split**: The data is split chronologically: the first 80% of sequences are used for training, and the final 20% for testing.
* **Compilation**:
    * **Optimizer**: `adam`
    * **Loss Function**: `mean_squared_error` (mse)
* **Callbacks**:
    * `EarlyStopping`: Monitors `val_loss` and stops training after 5 epochs of no improvement.
    * `ModelCheckpoint`: Saves only the best model based on `val_loss`.
* **Evaluation**: The primary metric is the Root Mean Squared Error (RMSE) calculated on the un-scaled temperature predictions.

### Saved Artifacts

* `best_climate_forecaster.keras`: The trained Keras model file.
* `weather_scaler.pkl`: The fitted `MinMaxScaler` instance, crucial for preprocessing input sequences and inverse-transforming the model's output.
* `feature_columns.json`: A list specifying the exact order of the 5 features the model was trained on.

### Usage (Inference)

* **Input**: A NumPy array of shape `(14, 5)` containing the scaled weather data for the last 14 days.
* **Preprocessing**: The raw data must be ordered correctly and scaled using the saved `weather_scaler.pkl`.
* **Output**: A dictionary containing the predicted values for each of the 5 features for the next day.