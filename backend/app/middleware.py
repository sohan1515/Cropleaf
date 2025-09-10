from django.http import HttpResponse
from django.conf import settings

class CustomCORSMiddleware:
    """
    Custom CORS middleware to handle CORS issues with credentials
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Only add CORS headers for API requests
        if request.path.startswith('/api/'):
            allowed_origins = getattr(settings, 'CORS_ALLOWED_ORIGINS', [])
            origin = request.META.get('HTTP_ORIGIN')

            if origin in allowed_origins:
                response['Access-Control-Allow-Origin'] = origin
                response['Access-Control-Allow-Credentials'] = 'true'
                response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
                response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'

                # Handle preflight requests
                if request.method == 'OPTIONS':
                    response['Access-Control-Max-Age'] = '86400'  # 24 hours

        return response