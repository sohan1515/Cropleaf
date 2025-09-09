from django.apps import AppConfig

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    def ready(self):
        # Import model to ensure it's loaded when Django starts
        # This helps with model initialization and signal connections
        try:
            from app import model
        except ImportError:
            # Handle case where model.py doesn't exist or has import errors
            pass