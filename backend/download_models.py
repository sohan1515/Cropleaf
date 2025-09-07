#!/usr/bin/env python
"""
Model Download Script for CropLeaf Deployment

This script helps download ML models from various sources for deployment.
Run this script during deployment to ensure models are available.

Usage:
    python download_models.py

Environment Variables:
    TF_MODEL_URL - Direct download URL for TensorFlow model
    TF_MODEL_GOOGLE_DRIVE_ID - Google Drive file ID for TensorFlow model
    TF_MODEL_FILENAME - Filename for TensorFlow model (default: CropLeaf-C1.h5)
    PT_MODEL_URL - Direct download URL for PyTorch model
    PT_MODEL_GOOGLE_DRIVE_ID - Google Drive file ID for PyTorch model
    PT_MODEL_FILENAME - Filename for PyTorch model (default: plant_disease_model_1_latest.pt)
"""

import os
import sys
import requests
from pathlib import Path

class ModelDownloader:
    def __init__(self):
        self.models_dir = Path(__file__).parent / "app" / "ml_models"
        self.models_dir.mkdir(parents=True, exist_ok=True)

    def download_from_google_drive(self, file_id, filename):
        """Download file from Google Drive"""
        try:
            url = f"https://drive.google.com/uc?export=download&id={file_id}"
            print(f"Downloading {filename} from Google Drive...")

            response = requests.get(url, stream=True, timeout=300)
            response.raise_for_status()

            filepath = self.models_dir / filename
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            print(f"✓ Successfully downloaded {filename}")
            return True

        except Exception as e:
            print(f"✗ Failed to download {filename} from Google Drive: {str(e)}")
            return False

    def download_from_url(self, url, filename):
        """Download file from direct URL"""
        try:
            print(f"Downloading {filename} from {url}...")

            response = requests.get(url, stream=True, timeout=300)
            response.raise_for_status()

            filepath = self.models_dir / filename
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)

            print(f"✓ Successfully downloaded {filename}")
            return True

        except Exception as e:
            print(f"✗ Failed to download {filename} from URL: {str(e)}")
            return False

    def download_models(self):
        """Download all configured models"""
        print("🚀 Starting model download process...")
        print(f"Models will be saved to: {self.models_dir}")

        # Get model filenames from environment variables with defaults
        tf_filename = os.getenv('TF_MODEL_FILENAME', 'CropLeaf-C1.h5')
        pt_filename = os.getenv('PT_MODEL_FILENAME', 'plant_disease_model_1_latest.pt')

        # TensorFlow model
        tf_downloaded = False
        tf_model_id = os.getenv('TF_MODEL_GOOGLE_DRIVE_ID')
        tf_model_url = os.getenv('TF_MODEL_URL')

        if tf_model_id:
            tf_downloaded = self.download_from_google_drive(tf_model_id, tf_filename)
        elif tf_model_url:
            tf_downloaded = self.download_from_url(tf_model_url, tf_filename)
        else:
            print("⚠️  No TensorFlow model download configuration found")

        # PyTorch model
        pt_downloaded = False
        pt_model_id = os.getenv('PT_MODEL_GOOGLE_DRIVE_ID')
        pt_model_url = os.getenv('PT_MODEL_URL')

        if pt_model_id:
            pt_downloaded = self.download_from_google_drive(pt_model_id, pt_filename)
        elif pt_model_url:
            pt_downloaded = self.download_from_url(pt_model_url, pt_filename)
        else:
            print("⚠️  No PyTorch model download configuration found")

        # Summary
        print("\n📋 Download Summary:")
        print(f"TensorFlow model: {'✓ Downloaded' if tf_downloaded else '✗ Not downloaded'}")
        print(f"PyTorch model: {'✓ Downloaded' if pt_downloaded else '✗ Not downloaded'}")

        if tf_downloaded or pt_downloaded:
            print("\n🎉 Model download completed successfully!")
            return True
        else:
            print("\n❌ No models were downloaded. Please configure download URLs.")
            return False

def main():
    """Main function"""
    print("CropLeaf Model Downloader")
    print("=" * 40)

    downloader = ModelDownloader()
    success = downloader.download_models()

    if not success:
        print("\n🔧 To configure model downloads, set these environment variables:")
        print("  TF_MODEL_GOOGLE_DRIVE_ID - Google Drive file ID for TensorFlow model")
        print("  TF_MODEL_URL - Direct download URL for TensorFlow model")
        print("  TF_MODEL_FILENAME - Filename for TensorFlow model (default: CropLeaf-C1.h5)")
        print("  PT_MODEL_GOOGLE_DRIVE_ID - Google Drive file ID for PyTorch model")
        print("  PT_MODEL_URL - Direct download URL for PyTorch model")
        print("  PT_MODEL_FILENAME - Filename for PyTorch model (default: plant_disease_model_1_latest.pt)")
        print("\n📖 See README.md for detailed setup instructions")
        sys.exit(1)

    sys.exit(0)

if __name__ == "__main__":
    main()