from django.contrib import admin
from .models import (
    Disease, Treatment, PreventionStrategy, FarmerProfile,
    PredictionHistory, DashboardStats, MandiLocation,
    MarketplaceProduct, ProductInquiry, Transaction,
    WeatherData, WeatherForecast, Notification, NotificationPreference
)

# Register your models here
admin.site.register(Disease)
admin.site.register(Treatment)
admin.site.register(PreventionStrategy)
admin.site.register(FarmerProfile)
admin.site.register(PredictionHistory)
admin.site.register(DashboardStats)
admin.site.register(MandiLocation)
admin.site.register(MarketplaceProduct)
admin.site.register(ProductInquiry)
admin.site.register(Transaction)
admin.site.register(WeatherData)
admin.site.register(WeatherForecast)
admin.site.register(Notification)
admin.site.register(NotificationPreference)

