# AgriSave ML Engine: Dataset Documentation

This document provides a detailed overview of the datasets used to train the machine learning models in the AgriSave application. Each section outlines the schema, features, and source of the data.

---

## 1. PlantVillage Disease Classification Dataset

This dataset is used to train the Convolutional Neural Network (CNN) for identifying diseases in plant leaves from images.

* **Purpose**: Image Classification (Crop Disease Detection)
* **Source**: [Kaggle - PlantVillage Dataset](https://www.kaggle.com/datasets/emmarex/plantdisease)
* **Model**: `disease_detection_model` (MobileNetV2)

### Schema and Features

The dataset is organized by directory, where each folder name represents the class label (the plant and its disease). The "features" are the pixel values of the images themselves.

* **Structure**: `/<PLANT>___<DISEASE_NAME>/<image_file.jpg>`
* **Image Properties**:
    * **Format**: `.jpg`
    * **Color Space**: RGB
    * **Dimensions**: Resized to `224x224` during preprocessing.

### Labels (Classes)

The model is trained to classify the following 15 categories:

1.  `Pepper__bell___Bacterial_spot`
2.  `Pepper__bell___healthy`
3.  `Potato___Early_blight`
4.  `Potato___Late_blight`
5.  `Potato___healthy`
6.  `Tomato_Bacterial_spot`
7.  `Tomato_Early_blight`
8.  `Tomato_Late_blight`
9.  `Tomato_Leaf_Mold`
10. `Tomato_Septoria_leaf_spot`
11. `Tomato_Spider_mites_Two_spotted_spider_mite`
12. `Tomato__Target_Spot`
13. `Tomato__Tomato_YellowLeaf__Curl_Virus`
14. `Tomato__Tomato_mosaic_virus`
15. `Tomato_healthy`

---

## 2. Crop Recommendation Dataset

This dataset provides optimal soil and atmospheric conditions for various crops. It's used to train a Random Forest Classifier to recommend the best crop to plant.

* **Purpose**: Tabular Classification (Crop Recommendation)
* **Source**: [Kaggle - Crop Recommendation Dataset](https://www.kaggle.com/datasets/atharvaingle/crop-recommendation-dataset)
* **Model**: `crop_recommendation_model` (Random Forest)

### Features

| Feature     | Data Type | Description                                           | Example Value |
| :---------- | :-------- | :---------------------------------------------------- | :------------ |
| `N`         | `integer` | Ratio of Nitrogen content in the soil.                | `90`          |
| `P`         | `integer` | Ratio of Phosphorous content in the soil.             | `42`          |
| `K`         | `integer` | Ratio of Potassium content in the soil.               | `43`          |
| `temperature` | `float`   | Temperature in degrees Celsius.                       | `20.87`       |
| `humidity`  | `float`   | Relative humidity in percentage.                      | `82.00`       |
| `ph`        | `float`   | pH value of the soil.                                 | `6.50`        |
| `rainfall`  | `float`   | Rainfall in millimeters (mm).                         | `202.93`      |
| `label`     | `string`  | **(Target Variable)** The name of the crop to recommend. | `rice`        |

---

## 3. Nairobi Weather Dataset

This is a time-series dataset containing historical weather data for Nairobi, Kenya. It's used to train a Long Short-Term Memory (LSTM) network to forecast future weather conditions.

* **Purpose**: Time-Series Forecasting (Climate Forecasting)
* **Source**: [Kaggle - Nairobi Weather Data](https://www.kaggle.com/datasets/johnkiriba/nairobi-weather-data)
* **Model**: `climate_forecasting_model` (LSTM)

### Features (Used in Training)

While the full dataset is rich, the model is trained on the following core features to predict the next day's weather conditions.

| Feature      | Data Type  | Description                                | Example Value |
| :----------- | :--------- | :----------------------------------------- | :------------ |
| `datetime`   | `datetime` | The date of the observation (used as index). | `2024-05-14`  |
| `temp`       | `float`    | Average temperature in Fahrenheit.         | `68.9`        |
| `humidity`   | `float`    | Relative humidity in percentage.           | `70.8`        |
| `precip`     | `float`    | Precipitation amount in inches.            | `0.0`         |
| `windspeed`  | `float`    | Wind speed in miles per hour.              | `13.6`        |
| `cloudcover` | `float`    | Percentage of the sky covered by clouds.   | `86.1`        |