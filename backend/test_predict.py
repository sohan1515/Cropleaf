#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CropLeaf.settings')
django.setup()

from app.utils import process_image
from django.core.files.storage import default_storage

def test_process_image():
    try:
        # Test with the existing test image
        test_image_path = 'test_image.jpg'
        if default_storage.exists(test_image_path):
            full_path = default_storage.path(test_image_path)
            print(f"Testing with image: {full_path}")
            result, max_probability, temp_files = process_image(full_path)
            print(f"Result: {result}")
            print(f"Max probability: {max_probability}")
            print(f"Temp files: {temp_files}")
        else:
            print("Test image not found")
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_process_image()