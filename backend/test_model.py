#!/usr/bin/env python
import os
import sys
import django

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CropLeaf.settings')
django.setup()

try:
    from app.model import model
    if model is None:
        print("ERROR: Model is None - failed to load")
    else:
        print("SUCCESS: Model loaded successfully")
        print(f"Model type: {type(model)}")
        print(f"Model summary: {model.summary()}")
except Exception as e:
    print(f"ERROR: Failed to import model: {str(e)}")
    import traceback
    traceback.print_exc()