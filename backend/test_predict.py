#!/usr/bin/env python
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CropLeaf.settings')
django.setup()

from django.http import JsonResponse, HttpRequest
from django.core.files.uploadedfile import SimpleUploadedFile
from app.views import predict_simple

def test_predict_function():
    """Test the predict function directly"""
    try:
        # Create a mock request
        request = HttpRequest()
        request.method = 'POST'

        # Create a simple test image
        from PIL import Image
        import io

        # Create a simple 100x100 gray image
        img = Image.new('RGB', (100, 100), color=(128, 128, 128))
        img_buffer = io.BytesIO()
        img.save(img_buffer, format='JPEG')
        img_buffer.seek(0)

        # Create a SimpleUploadedFile
        test_image = SimpleUploadedFile(
            "test_image.jpg",
            img_buffer.getvalue(),
            content_type="image/jpeg"
        )

        # Add the file to the request
        request.FILES['image'] = test_image

        print("Testing predict function with mock request...")

        # Call the predict function
        response = predict_simple(request)

        print("Response status:", response.status_code)
        print("Response content:", response.content.decode('utf-8'))

        return response

    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_predict_function()