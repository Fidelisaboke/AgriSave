"""
This module implements the training pipeline for a crop disease detection model using
transfer learning with MobileNetV2.
"""

import json
import logging
from pathlib import Path

import tensorflow as tf
from django.conf import settings
from keras.applications import MobileNetV2
from keras.callbacks import ModelCheckpoint, EarlyStopping
from keras.layers import GlobalAveragePooling2D, RandomFlip, RandomRotation, RandomZoom, Dense, Dropout
from keras.models import Sequential
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer

from ..models import DiseaseDetector
from ..utils import fetch_image_paths_from_directory

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def parse_image(filename, label):
    """
    Reads and preprocesses an image from a file path.
    """
    image_string = tf.io.read_file(filename)
    image = tf.image.decode_jpeg(image_string, channels=3)
    image = tf.image.resize(image, [224, 224])
    image = image / 255.0
    return image, label


def configure_dataset(filenames, labels, shuffle=False):
    """
    Configures a tf.data.Dataset for training or evaluation.
    """
    dataset = tf.data.Dataset.from_tensor_slices((filenames, labels))
    if shuffle:
        dataset = dataset.shuffle(buffer_size=len(filenames))
    dataset = dataset.map(parse_image, num_parallel_calls=tf.data.AUTOTUNE)
    dataset = dataset.batch(16)
    dataset = dataset.prefetch(buffer_size=tf.data.AUTOTUNE)
    return dataset


def run_disease_detection_training():
    """
    Orchestrates the training process for the disease detection model.
    """
    # Load and preprocess data
    dataset_root = Path(settings.DATASETS_DIR) / "raw/PlantVillage/"
    image_paths, image_labels, class_names = fetch_image_paths_from_directory(dataset_root)

    if not image_paths:
        logging.error("Training stopped: No images found.")
        return

    # Save the discovered class names for inference later
    model_save_dir = Path(settings.ML_MODELS_DIR) / "disease_detection/"
    model_save_dir.mkdir(parents=True, exist_ok=True)

    # Save class names to a JSON file
    with open(model_save_dir / "class_names.json", 'w') as f:
        json.dump(class_names, f)
    logging.info(f"[SUCCESS] Saved class names to {model_save_dir / 'class_names.json'}")

    # Label Binarization
    label_binarizer = LabelBinarizer()
    image_labels_scaled = label_binarizer.fit_transform(image_labels)

    # Split paths and labels into training and validation sets
    X_train_paths, X_test_paths, y_train, y_test = train_test_split(
        image_paths,
        image_labels_scaled,
        test_size=0.2,
        random_state=42,
        stratify=image_labels
    )
    logging.info(f"Data split: {len(X_train_paths)} training images, {len(X_test_paths)} validation images.")

    # Train and validation datasets
    train_dataset = configure_dataset(X_train_paths, y_train, shuffle=True)
    val_dataset = configure_dataset(X_test_paths, y_test, shuffle=False)

    # Load the MobileNetV2 base model
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    base_model.trainable = False

    # Build the model
    model = Sequential([
        # Data augmentation layers
        RandomFlip("horizontal"),
        RandomRotation(0.1),
        RandomZoom(0.1),

        # Pre-trained base model
        base_model,

        # Classification head
        GlobalAveragePooling2D(),
        Dropout(0.2),
        Dense(len(class_names), activation='softmax')
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    model.summary()

    # Save best model during training
    checkpoint_path = model_save_dir / "best_disease_detector.keras"
    checkpoint = ModelCheckpoint(str(checkpoint_path), monitor='val_accuracy', save_best_only=True)
    early_stopping = EarlyStopping(monitor='val_accuracy', patience=3, restore_best_weights=True)

    # Train the model
    model.fit(
        train_dataset,
        validation_data=val_dataset,
        epochs=15,
        callbacks=[checkpoint, early_stopping]
    )

    # Evaluate the model
    try:
        loss, accuracy = model.evaluate(val_dataset)
        logging.info(f"Validation Loss: {loss:.4f}, Validation Accuracy: {accuracy:.4f}")
    except Exception as e:
        logging.error(f"Error during model evaluation: {e}")
        loss, accuracy = float('inf'), 0.0

    # Save the training job metadata to the database
    relative_path = checkpoint_path.relative_to(settings.MEDIA_ROOT)
    DiseaseDetector.objects.create(
        name="Disease Detector",
        version="1.0",
        model_file=str(relative_path),
        metrics={
            "validation_loss": float(loss),
            "validation_accuracy": float(accuracy)
        },
    )
    logging.info(f"[SUCCESS] Saved trained model metadata to the database.")
