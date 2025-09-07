#!/usr/bin/env python
import requests
import os

# Test the API endpoint
url = 'http://localhost:8000/api/predict/'

# Create a simple test image (just for testing the endpoint)
test_image_path = 'test_image.jpg'
if not os.path.exists(test_image_path):
    # Create a simple 256x256 white image for testing
    from PIL import Image
    img = Image.new('RGB', (256, 256), color='white')
    img.save(test_image_path)

try:
    with open(test_image_path, 'rb') as f:
        files = {'image': f}
        response = requests.post(url, files=files)

    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")

    if response.status_code == 200:
        print("✅ API endpoint is working!")
    else:
        print("❌ API endpoint returned an error")

except Exception as e:
    print(f"❌ Error testing API: {str(e)}")

# Clean up
if os.path.exists(test_image_path):
    os.remove(test_image_path)