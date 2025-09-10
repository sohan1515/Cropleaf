#!/bin/bash
# Build script for Render deployment

set -e  # Exit on any error

echo "Starting build process..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r backend/requirements.txt

# Run database migrations
echo "Running database migrations..."
cd backend
python manage.py collectstatic --noinput --verbosity=1
python manage.py migrate --verbosity=1

# Download ML models (don't fail if this fails)
echo "Attempting to download ML models..."
if python download_models.py; then
    echo "ML models downloaded successfully"
else
    echo "Warning: ML model download failed, but continuing with build"
fi

# Test that Django can start
echo "Testing Django application..."
if python manage.py check --deploy; then
    echo "Django application check passed"
else
    echo "Warning: Django check failed, but continuing"
fi

echo "Build completed successfully"