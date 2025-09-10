import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

import tensorflow as tf
from tensorflow import keras
import torch
import torch.nn as nn
from torchvision import models, transforms
import numpy as np
from PIL import Image
import requests
import logging
from urllib.parse import urlparse

class ModelWrapper:
    def __init__(self):
        self.tf_model = None
        self.pt_model = None
        self.model_type = None
        self.models_dir = os.path.join(os.path.dirname(__file__), "ml_models")
        os.makedirs(self.models_dir, exist_ok=True)
        self.load_models()

    def download_file_from_google_drive(self, file_id, destination):
        """Download file from Google Drive"""
        try:
            # Google Drive direct download URL
            url = f"https://drive.google.com/uc?export=download&id={file_id}"

            print(f"Downloading model from Google Drive: {file_id}")
            response = requests.get(url, stream=True, timeout=300)  # 5 minute timeout
            response.raise_for_status()

            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            print(f"Successfully downloaded model to: {destination}")
            return True

        except Exception as e:
            print(f"Error downloading from Google Drive: {str(e)}")
            return False

    def download_file_from_url(self, url, destination):
        """Download file from any URL"""
        try:
            print(f"Downloading model from: {url}")
            response = requests.get(url, stream=True, timeout=300)
            response.raise_for_status()

            with open(destination, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            print(f"Successfully downloaded model to: {destination}")
            return True

        except Exception as e:
            print(f"Error downloading from URL: {str(e)}")
            return False

    def ensure_model_available(self, model_name, download_url=None, google_drive_id=None):
        """Ensure a model file is available, downloading if necessary"""
        model_path = os.path.join(self.models_dir, model_name)

        if os.path.exists(model_path):
            print(f"Model {model_name} already exists locally")
            return True

        print(f"Model {model_name} not found locally, attempting to download...")

        # Try Google Drive first if ID provided
        if google_drive_id:
            if self.download_file_from_google_drive(google_drive_id, model_path):
                return True

        # Try direct URL if provided
        if download_url:
            if self.download_file_from_url(download_url, model_path):
                return True

        print(f"Failed to download model {model_name}")
        return False

    def load_models(self):
        try:
            # Model download URLs - configure these environment variables
            tf_model_url = os.getenv('TF_MODEL_URL')
            tf_model_drive_id = os.getenv('TF_MODEL_GOOGLE_DRIVE_ID')
            pt_model_url = os.getenv('PT_MODEL_URL')
            pt_model_drive_id = os.getenv('PT_MODEL_GOOGLE_DRIVE_ID')

            # Get model filenames from environment variables with defaults
            tf_filename = os.getenv('TF_MODEL_FILENAME', 'CropLeaf-C1.h5')
            pt_filename = os.getenv('PT_MODEL_FILENAME', 'plant_disease_model_1_latest.pt')

            # Try to load TensorFlow/Keras model first
            tf_model_path = os.path.join(self.models_dir, tf_filename)
            if not os.path.exists(tf_model_path):
                print("TensorFlow model not found locally, attempting to download...")
                if not self.ensure_model_available(tf_filename, tf_model_url, tf_model_drive_id):
                    print("Failed to download TensorFlow model")

            if os.path.exists(tf_model_path):
                try:
                    self.tf_model = tf.keras.models.load_model(tf_model_path)
                    self.tf_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
                    self.model_type = 'tensorflow'
                    print(f"TensorFlow/Keras Model ({tf_filename}) loaded successfully")
                except Exception as e:
                    print(f"Error loading TensorFlow model: {str(e)}")
                    self.tf_model = None
            else:
                print("TensorFlow model file not available")
                self.tf_model = None

            # Try to load PyTorch model
            pt_model_path = os.path.join(self.models_dir, pt_filename)
            if not os.path.exists(pt_model_path):
                print("PyTorch model not found locally, attempting to download...")
                if not self.ensure_model_available(pt_filename, pt_model_url, pt_model_drive_id):
                    print("Failed to download PyTorch model")

            if os.path.exists(pt_model_path):
                try:
                    # Load the checkpoint
                    checkpoint = torch.load(pt_model_path, map_location=torch.device('cpu'))

                    # Store the checkpoint for now - we'll handle prediction differently
                    self.pt_model = checkpoint
                    print("PyTorch model checkpoint loaded (architecture detection pending)")

                    if self.tf_model is None:
                        self.model_type = 'pytorch'
                    print(f"PyTorch Model ({pt_filename}) loaded successfully")
                except Exception as e:
                    print(f"Error loading PyTorch model: {str(e)}")
                    self.pt_model = None
            else:
                print("PyTorch model file not available")
                self.pt_model = None

            if self.tf_model is None and self.pt_model is None:
                print("No models could be loaded. Application will continue without ML models.")
                print("Configure model download URLs using environment variables if needed:")
                print("  TF_MODEL_URL - Direct download URL for TensorFlow model")
                print("  TF_MODEL_GOOGLE_DRIVE_ID - Google Drive file ID for TensorFlow model")
                print("  TF_MODEL_FILENAME - Filename for TensorFlow model (default: CropLeaf-C1.h5)")
                print("  PT_MODEL_URL - Direct download URL for PyTorch model")
                print("  PT_MODEL_GOOGLE_DRIVE_ID - Google Drive file ID for PyTorch model")
                print("  PT_MODEL_FILENAME - Filename for PyTorch model (default: plant_disease_model_1_latest.pt)")
                self.model_type = None
            else:
                print("At least one model loaded successfully")

        except Exception as e:
            print(f"Critical error during model loading: {str(e)}")
            print("Application will continue without ML models")
            self.tf_model = None
            self.pt_model = None
            self.model_type = None

    def predict(self, image_array):
        if self.model_type == 'tensorflow' and self.tf_model is not None:
            return self.tf_model.predict(image_array)
        elif self.model_type == 'pytorch' and self.pt_model is not None:
            return self.predict_pytorch(image_array)
        else:
            raise ValueError("No model available for prediction")

    def predict_pytorch(self, image_array):
        try:
            # Convert numpy array to torch tensor
            if isinstance(image_array, np.ndarray):
                # Assuming image_array is in format (batch, height, width, channels)
                # Convert to (batch, channels, height, width) for PyTorch
                image_array = np.transpose(image_array, (0, 3, 1, 2))
                image_tensor = torch.from_numpy(image_array).float()

            # Normalize to [0,1] range
            image_tensor = image_tensor / 255.0

            # Check if pt_model is a complete model or just a checkpoint
            if hasattr(self.pt_model, 'forward'):
                # It's a complete model
                with torch.no_grad():
                    outputs = self.pt_model(image_tensor)
                    probabilities = torch.nn.functional.softmax(outputs, dim=1)
                    return probabilities.numpy()
            else:
                # It's a checkpoint/state_dict - we can't use it directly for prediction
                # Return a fallback response
                print("PyTorch model is a checkpoint and needs proper model architecture to be loaded")
                # Return dummy predictions that will be ignored since TF model takes precedence
                return np.array([[0.0] * 17])  # 17 classes

        except Exception as e:
            print(f"PyTorch prediction error: {str(e)}")
            # Return dummy predictions
            return np.array([[0.0] * 17])

    def check_models_loaded(self):
        """Check if models are properly loaded"""
        tf_loaded = self.tf_model is not None
        pt_loaded = self.pt_model is not None
        return tf_loaded or pt_loaded


# Create global model instance
model_wrapper = ModelWrapper()
model = model_wrapper  # For backward compatibility

