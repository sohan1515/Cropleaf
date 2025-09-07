from django.urls import path
from django.conf import settings
from django.conf.urls import handler404
from django.conf.urls.static import static
from app.views import login_view , register_view, logout_view ,home , profiledata , crops ,contact_view, uploads, forgot_pass, my_404_page, PredictView, disease_details, translate_text, dashboard_stats, farmer_dashboard, api_login, api_register, marketplace_products, mandi_locations, verify_product_quality, create_product_inquiry, get_weather_data, get_weather_forecast, get_user_notifications, create_notification, update_notification_preferences, get_notification_preferences, health_check

handler404 = my_404_page

urlpatterns = [
    path('',home,name="home"),
    path('upload/', uploads, name='upload'),
    path('crops/',crops,name="crops"),
    path('crops/disease/<slug:oneDisease>/', crops, name='oneDisease'),
    path('forgot-password/',forgot_pass,name="forgot"),
    path('register/',register_view,name="register"),
    path('contact/', contact_view, name='contact'),
    path('login/',login_view,name="login"),
    path('logout/',logout_view, name='logout'),
    path('user/profile/<int:pk>/',profiledata, name='profile'),
    path('api/predict/', PredictView.as_view(), name='api_predict'),
    path('api/disease/<str:disease_name>/', disease_details, name='disease_details'),
    path('api/translate/', translate_text, name='translate_text'),
    path('api/dashboard/stats/', dashboard_stats, name='dashboard_stats'),
    path('api/dashboard/farmer/', farmer_dashboard, name='farmer_dashboard'),
    path('api/auth/login/', api_login, name='api_login'),
    path('api/auth/register/', api_register, name='api_register'),
    path('api/marketplace/products/', marketplace_products, name='marketplace_products'),
    path('api/marketplace/mandis/', mandi_locations, name='mandi_locations'),
    path('api/marketplace/verify-quality/', verify_product_quality, name='verify_product_quality'),
    path('api/marketplace/inquiry/', create_product_inquiry, name='create_product_inquiry'),

    # Weather and Notifications
    path('api/weather/current/', get_weather_data, name='get_weather_data'),
    path('api/weather/forecast/', get_weather_forecast, name='get_weather_forecast'),
    path('api/notifications/', get_user_notifications, name='get_user_notifications'),
    path('api/notifications/create/', create_notification, name='create_notification'),
    path('api/notifications/preferences/', get_notification_preferences, name='get_notification_preferences'),
    path('api/notifications/preferences/update/', update_notification_preferences, name='update_notification_preferences'),

    # Health check for Render monitoring
    path('api/health/', health_check, name='health_check'),
]