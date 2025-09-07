#!/bin/bash
# Build script for Render deployment

# Install Python dependencies
pip install -r backend/requirements.txt

# Run database migrations
cd backend
python manage.py collectstatic --noinput
python manage.py migrate

# Download ML models
python download_models.py

echo "Build completed successfully"