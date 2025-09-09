from django.contrib import admin
from django.urls import path , include
from app import urls as app_urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(app_urls)),
]

# Static files are handled by WhiteNoise in production
# Only serve static files in development (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)