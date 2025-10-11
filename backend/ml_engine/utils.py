"""
Utility functions for ML Engine
These will be used when integrating real ML models
"""
import logging
import os
from pathlib import Path

from .constants import DISEASE_RECOMMENDATIONS

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def fetch_image_paths_from_directory(dataset_path: Path) -> tuple:
    """
    Scans a directory to load image paths and their corresponding labels.

    This function assumes a directory structure where each subdirectory
    represents a class name and contains the images for that class.

    Args:
        dataset_path (str): The path to the root dataset directory.

    Returns:
        tuple: A tuple containing:
            - list: A list of image paths.
            - list: A list of integer labels corresponding to each image.
            - list: A sorted list of class names found in the directory.
    """
    image_paths = []
    labels = []

    if not dataset_path.is_dir():
        logging.error(f"Dataset path '{dataset_path}' does not exist or is not a directory.")
        return [], [], []

    # Discover and sort class names from the folder names
    class_names = sorted([d.name for d in os.scandir(dataset_path) if d.is_dir()])
    if not class_names:
        logging.warning(f"No subdirectories found in '{dataset_path}'. No classes to load.")
        return [], [], []

    logging.info(f"Found {len(class_names)} classes: {class_names}")

    # Create a mapping from class name to integer index
    class_to_idx = {name: i for i, name in enumerate(class_names)}

    # Iterate over each class directory
    for class_name in class_names:
        class_dir = dataset_path / class_name
        image_extensions = ["*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"]
        files_found = []

        for ext in image_extensions:
            files_found.extend(class_dir.glob(ext))

        for image_file in files_found:
            image_paths.append(str(image_file))
            labels.append(class_to_idx[class_name])

    logging.info(f"Successfully loaded {len(image_paths)} images and {len(labels)} labels.")
    return image_paths, labels, class_names

def is_plant_healthy(predicted_class):
    """Check if the predicted class indicates a healthy plant."""
    return "healthy" in predicted_class.lower()

def calculate_severity(confidence):
    """Calculate severity based on confidence score."""
    if confidence >= 0.9:
        return "Critical"
    elif confidence >= 0.75:
        return "High"
    elif confidence >= 0.5:
        return "Medium"
    else:
        return "Low"

def get_recommendation_for_class(predicted_class):
    """Fetch recommendations for a given disease class."""
    if predicted_class in DISEASE_RECOMMENDATIONS:
        return DISEASE_RECOMMENDATIONS[predicted_class]["steps"]
        
    return None
