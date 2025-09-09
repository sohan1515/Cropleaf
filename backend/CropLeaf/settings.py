import os
from pathlib import Path
import requests

def download_file_from_google_drive(file_id, filepath):
    """Download file from Google Drive"""
    if not file_id:
        return False
    try:
        # Handle both full URLs and file IDs
        if "drive.google.com" in file_id:
            # Extract file ID from URL - handle both /file/d/ and /open?id= formats
            import re
            match = re.search(r'/file/d/([a-zA-Z0-9_-]+)', file_id)
            if not match:
                match = re.search(r'[?&]id=([a-zA-Z0-9_-]+)', file_id)
            if match:
                file_id = match.group(1)
            else:
                print(f"❌ Could not extract file ID from URL: {file_id}")
                return False

        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        print(f"Downloading model from Google Drive (ID: {file_id}): {filepath}")

        response = requests.get(url, stream=True, timeout=300)
        response.raise_for_status()

        with open(filepath, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        print(f"Downloaded successfully: {filepath}")
        return True
    except Exception as e:
        print(f"❌ Failed to download {filepath} from Google Drive: {e}")
        return False

def download_file(url, filepath, google_drive_id=None):
    """Download a file from a URL or Google Drive if not already present."""
    if os.path.exists(filepath):
        print(f"✅ Model already exists: {filepath}")
        return

    # Try Google Drive first if ID provided
    if google_drive_id:
        if download_file_from_google_drive(google_drive_id, filepath):
            return

    # Try direct URL if provided
    if url:
        print(f"Downloading model: {filepath}")
        try:
            response = requests.get(url, stream=True, timeout=300)
            response.raise_for_status()
            with open(filepath, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            print(f"Downloaded successfully: {filepath}")
        except Exception as e:
            print(f"❌ Failed to download {filepath}: {e}")
    else:
        print(f"URL not provided for {filepath}")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    env_path = BASE_DIR / '.env'
    if env_path.exists():
        load_dotenv(env_path)
        print(f"✅ Loaded environment variables from {env_path}")
    else:
        print(f"⚠️  .env file not found at {env_path}")
except ImportError:
    print("⚠️  python-dotenv not installed, using system environment variables only")

TF_MODEL_URL = os.getenv("TF_MODEL_URL")
PT_MODEL_URL = os.getenv("PT_MODEL_URL")
TF_MODEL_GOOGLE_DRIVE_ID = os.getenv("TF_MODEL_GOOGLE_DRIVE_ID")
PT_MODEL_GOOGLE_DRIVE_ID = os.getenv("PT_MODEL_GOOGLE_DRIVE_ID")

# Debug: Print environment variables
print("=== Model Download Configuration ===")
print(f"TF_MODEL_URL: {TF_MODEL_URL}")
print(f"PT_MODEL_URL: {PT_MODEL_URL}")
print(f"TF_MODEL_GOOGLE_DRIVE_ID: {TF_MODEL_GOOGLE_DRIVE_ID}")
print(f"PT_MODEL_GOOGLE_DRIVE_ID: {PT_MODEL_GOOGLE_DRIVE_ID}")
print("===================================")

# Model file paths - use same directory as model.py (backend/app/ml_models)
APP_DIR = BASE_DIR / "app"
ML_MODELS_DIR = APP_DIR / "ml_models"

# Get model filenames from environment variables with defaults
TF_MODEL_FILENAME = os.getenv('TF_MODEL_FILENAME', 'CropLeaf-C1.h5')
PT_MODEL_FILENAME = os.getenv('PT_MODEL_FILENAME', 'plant_disease_model_1_latest.pt')

TF_MODEL_FILE = ML_MODELS_DIR / TF_MODEL_FILENAME
PT_MODEL_FILE = ML_MODELS_DIR / PT_MODEL_FILENAME

# Model download is now handled by the download_models.py script during deployment
# and by the ModelWrapper class when needed
# This prevents startup issues if models can't be downloaded immediately

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-l8**w9!+h)4(8wdl!w#y)h35khdnbec5marktpz#%wz&i4+ooj')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,your-project-name.onrender.com').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_recaptcha',
    'rest_framework',
    'corsheaders',
    'app',
]


RECAPTCHA_PUBLIC_KEY = '6LeApmMrAAAAANKwRdcDDO9jybdrN1EX7EyxdAfq'

RECAPTCHA_PRIVATE_KEY = '6LeApmMrAAAAAK3WKQP-hZR0r5rFrm5SHLlkl1jA'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',  # Temporarily disabled for API
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'CropLeaf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'CropLeaf.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'crop_leaf'),
        'USER': os.getenv('DB_USER', 'postgres'),
        'PASSWORD': os.getenv('DB_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
        'OPTIONS': {
            'sslmode': 'require' if os.getenv('DB_SSL', 'false').lower() == 'true' else 'disable',
        }
    }
}

# Fallback to SQLite for local development
if not os.getenv('DB_HOST'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# WhiteNoise configuration
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MEDIA_ROOT = BASE_DIR / 'media'


LOGIN_URL = '/login/'

CSP_SCRIPT_SRC = ("'self'", "https://translate.google.com")

CSP_FRAME_SRC = ("'self'", "https://translate.google.com")

# set this on cmd for ignore warnings
# export TF_CPP_MIN_LOG_LEVEL=2
# set TF_ENABLE_ONEDNN_OPTS=0

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:5173',
    'http://localhost:5174',
    'http://localhost:5175',
    'http://192.168.1.13:5173',
    'https://your-project-name.onrender.com',
]

# CSRF trusted origins for Django 4.0+
CSRF_TRUSTED_ORIGINS = [
    'http://localhost:3000',
    'http://localhost:5173',
    'http://localhost:5174',
    'http://localhost:5175',
    'http://192.168.1.13:5173',
    'https://your-project-name.onrender.com',
]

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# Django REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [],
}
