from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User

class Disease(models.Model):
    SEVERITY_CHOICES = [
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('severe', 'Severe'),
    ]

    name = models.CharField(max_length=100, unique=True)
    scientific_name = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    affected_crops = models.JSONField()
    severity_levels = models.JSONField(default=dict)  # mild, moderate, severe
    symptoms = models.JSONField(default=list)

    # Enhanced fields for comprehensive disease information
    causal_agent = models.CharField(max_length=200, blank=True, help_text="Bacteria, fungus, virus, etc.")
    host_range = models.TextField(blank=True, help_text="Which crops/plant species are affected")
    environmental_conditions = models.TextField(blank=True, help_text="Temperature, humidity requirements for disease development")
    disease_cycle = models.TextField(blank=True, help_text="How the disease spreads and develops")
    economic_impact = models.TextField(blank=True, help_text="Yield loss, economic damage information")

    # Management information
    cultural_control = models.TextField(blank=True, help_text="Cultural practices for disease management")
    chemical_control = models.TextField(blank=True, help_text="Chemical treatment options")
    biological_control = models.TextField(blank=True, help_text="Biological control methods")
    integrated_management = models.TextField(blank=True, help_text="IPM strategies")

    # Additional metadata
    references = models.TextField(blank=True, help_text="Scientific references and sources")
    images = models.JSONField(default=list, help_text="Image URLs for disease symptoms")
    prevention_priority = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        default='moderate',
        help_text="Priority level for prevention"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Disease"
        verbose_name_plural = "Diseases"
        ordering = ['name']

class Treatment(models.Model):
    TREATMENT_TYPES = [
        ('chemical', 'Chemical'),
        ('organic', 'Organic'),
        ('biological', 'Biological'),
        ('cultural', 'Cultural'),
        ('preventive', 'Preventive'),
    ]

    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='treatments')
    name = models.CharField(max_length=200)
    description = models.TextField()
    treatment_type = models.CharField(max_length=20, choices=TREATMENT_TYPES)
    effectiveness_rating = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Effectiveness rating from 1-5"
    )
    application_method = models.TextField()
    safety_precautions = models.TextField(blank=True)
    cost_estimate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="Estimated cost per application"
    )
    duration_days = models.IntegerField(
        null=True,
        blank=True,
        help_text="How long the treatment takes to show results"
    )
    regional_availability = models.JSONField(
        default=dict,
        help_text="Availability by region/country"
    )
    is_recommended = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.disease.name} - {self.name}"

    class Meta:
        verbose_name = "Treatment"
        verbose_name_plural = "Treatments"
        ordering = ['-effectiveness_rating', 'cost_estimate']

class PreventionStrategy(models.Model):
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='preventions')
    title = models.CharField(max_length=200)
    description = models.TextField()
    strategy_type = models.CharField(max_length=50)  # crop_rotation, irrigation, etc.
    implementation_steps = models.JSONField(default=list)
    expected_benefits = models.TextField()
    difficulty_level = models.CharField(
        max_length=20,
        choices=[
            ('easy', 'Easy'),
            ('moderate', 'Moderate'),
            ('difficult', 'Difficult'),
        ],
        default='moderate'
    )
    cost_impact = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low Cost'),
            ('medium', 'Medium Cost'),
            ('high', 'High Cost'),
        ],
        default='low'
    )

    def __str__(self):
        return f"{self.disease.name} - {self.title}"

    class Meta:
        verbose_name = "Prevention Strategy"
        verbose_name_plural = "Prevention Strategies"

class TreatmentFeedback(models.Model):
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE, related_name='feedback')
    user_rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    effectiveness_observed = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comments = models.TextField(blank=True)
    farmer_location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Treatment Feedback"
        verbose_name_plural = "Treatment Feedback"

class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    farm_name = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    farm_size = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Farm size in acres/hectares")
    primary_crops = models.JSONField(default=list, help_text="List of primary crops grown")
    experience_years = models.IntegerField(null=True, blank=True)
    contact_number = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    class Meta:
        verbose_name = "Farmer Profile"
        verbose_name_plural = "Farmer Profiles"

class PredictionHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions', null=True, blank=True)
    disease = models.ForeignKey(Disease, on_delete=models.CASCADE, related_name='predictions')
    confidence_score = models.DecimalField(max_digits=5, decimal_places=4, validators=[MinValueValidator(0), MaxValueValidator(1)])
    image_path = models.CharField(max_length=500, blank=True)
    location = models.CharField(max_length=200, blank=True, help_text="Location where prediction was made")
    crop_type = models.CharField(max_length=100, blank=True)
    weather_conditions = models.JSONField(default=dict, help_text="Weather data at time of prediction")
    treatment_applied = models.ForeignKey(Treatment, on_delete=models.SET_NULL, null=True, blank=True)
    treatment_effectiveness = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)])
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.disease.name} - {self.created_at.date()}"

    class Meta:
        verbose_name = "Prediction History"
        verbose_name_plural = "Prediction Histories"
        ordering = ['-created_at']

class DashboardStats(models.Model):
    date = models.DateField(unique=True)
    total_predictions = models.IntegerField(default=0)
    disease_counts = models.JSONField(default=dict, help_text="Count of each disease detected")
    crop_distribution = models.JSONField(default=dict, help_text="Distribution of crops analyzed")
    region_stats = models.JSONField(default=dict, help_text="Statistics by region")
    treatment_effectiveness = models.JSONField(default=dict, help_text="Average treatment effectiveness ratings")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Dashboard Stats - {self.date}"

    class Meta:
        verbose_name = "Dashboard Statistics"
        verbose_name_plural = "Dashboard Statistics"
        ordering = ['-date']

# Marketplace Models
class MandiLocation(models.Model):
    name = models.CharField(max_length=200)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    address = models.TextField()
    contact_number = models.CharField(max_length=20, blank=True)
    operating_hours = models.CharField(max_length=200, blank=True)
    facilities = models.JSONField(default=list, help_text="Available facilities at the mandi")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name}, {self.district}"

    class Meta:
        verbose_name = "Mandi Location"
        verbose_name_plural = "Mandi Locations"

class MarketplaceProduct(models.Model):
    PRODUCT_TYPES = [
        ('crop', 'Crop'),
        ('seed', 'Seed'),
        ('fertilizer', 'Fertilizer'),
        ('equipment', 'Equipment'),
        ('other', 'Other'),
    ]

    QUALITY_GRADES = [
        ('a', 'Grade A'),
        ('b', 'Grade B'),
        ('c', 'Grade C'),
        ('ungraded', 'Ungraded'),
    ]

    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products')
    title = models.CharField(max_length=200)
    description = models.TextField()
    product_type = models.CharField(max_length=20, choices=PRODUCT_TYPES, default='crop')
    category = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Quantity in kg/liters/units")
    unit = models.CharField(max_length=20, default='kg')
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # Location and logistics
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    nearest_mandi = models.ForeignKey(MandiLocation, on_delete=models.SET_NULL, null=True, blank=True)

    # Quality verification
    quality_grade = models.CharField(max_length=20, choices=QUALITY_GRADES, default='ungraded')
    ai_verified = models.BooleanField(default=False)
    ai_confidence_score = models.DecimalField(max_digits=5, decimal_places=4, blank=True, null=True)
    disease_detected = models.CharField(max_length=200, blank=True)
    quality_certificate_url = models.URLField(blank=True)

    # Images
    images = models.JSONField(default=list, help_text="List of image URLs")

    # Status
    is_active = models.BooleanField(default=True)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.quantity and self.price_per_unit:
            self.total_price = self.quantity * self.price_per_unit
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} - {self.seller.username}"

    class Meta:
        verbose_name = "Marketplace Product"
        verbose_name_plural = "Marketplace Products"
        ordering = ['-created_at']

class ProductInquiry(models.Model):
    product = models.ForeignKey(MarketplaceProduct, on_delete=models.CASCADE, related_name='inquiries')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='inquiries')
    message = models.TextField()
    contact_number = models.CharField(max_length=20, blank=True)
    quantity_needed = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    proposed_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry for {self.product.title} by {self.buyer.username}"

    class Meta:
        verbose_name = "Product Inquiry"
        verbose_name_plural = "Product Inquiries"
        ordering = ['-created_at']

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    product = models.ForeignKey(MarketplaceProduct, on_delete=models.CASCADE, related_name='transactions')
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchases')
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sales')

    quantity_purchased = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_date = models.DateTimeField(auto_now_add=True)
    delivery_date = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.product.title} - {self.buyer.username} to {self.seller.username}"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"
        ordering = ['-transaction_date']

# Weather and Notifications Models
class WeatherData(models.Model):
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)

    # Current weather
    temperature = models.DecimalField(max_digits=5, decimal_places=2, help_text="Temperature in Celsius")
    humidity = models.IntegerField(help_text="Humidity percentage")
    pressure = models.IntegerField(help_text="Pressure in hPa")
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, help_text="Wind speed in m/s")
    wind_direction = models.IntegerField(help_text="Wind direction in degrees")
    weather_condition = models.CharField(max_length=100)
    weather_description = models.CharField(max_length=200)
    weather_icon = models.CharField(max_length=10)

    # Additional data
    visibility = models.IntegerField(blank=True, null=True, help_text="Visibility in meters")
    uv_index = models.DecimalField(max_digits=3, decimal_places=1, blank=True, null=True)
    dew_point = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    # Timestamps
    recorded_at = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Weather in {self.location} - {self.temperature}°C"

    class Meta:
        verbose_name = "Weather Data"
        verbose_name_plural = "Weather Data"
        ordering = ['-recorded_at']
        indexes = [
            models.Index(fields=['location', '-recorded_at']),
            models.Index(fields=['latitude', 'longitude']),
        ]

class WeatherForecast(models.Model):
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)

    # Forecast data
    forecast_date = models.DateField()
    forecast_time = models.TimeField()

    temperature = models.DecimalField(max_digits=5, decimal_places=2)
    temperature_min = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    temperature_max = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    humidity = models.IntegerField()
    pressure = models.IntegerField()
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2)
    wind_direction = models.IntegerField()
    weather_condition = models.CharField(max_length=100)
    weather_description = models.CharField(max_length=200)
    weather_icon = models.CharField(max_length=10)

    # Precipitation
    precipitation_probability = models.IntegerField(default=0, help_text="Probability of precipitation %")
    precipitation_amount = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Precipitation amount in mm")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Forecast for {self.location} - {self.forecast_date}"

    class Meta:
        verbose_name = "Weather Forecast"
        verbose_name_plural = "Weather Forecasts"
        ordering = ['forecast_date', 'forecast_time']
        indexes = [
            models.Index(fields=['location', 'forecast_date']),
            models.Index(fields=['latitude', 'longitude', 'forecast_date']),
        ]

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('weather', 'Weather Alert'),
        ('disease', 'Disease Alert'),
        ('market', 'Market Alert'),
        ('treatment', 'Treatment Reminder'),
        ('system', 'System Notification'),
    ]

    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='medium')

    # Additional data
    data = models.JSONField(default=dict, help_text="Additional notification data")

    # Status
    is_read = models.BooleanField(default=False)
    is_sent = models.BooleanField(default=False)

    # Scheduling
    scheduled_at = models.DateTimeField(blank=True, null=True)
    sent_at = models.DateTimeField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.notification_type}: {self.title}"

    class Meta:
        verbose_name = "Notification"
        verbose_name_plural = "Notifications"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['notification_type', 'is_read']),
            models.Index(fields=['scheduled_at']),
        ]

class NotificationPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='notification_preferences')

    # Weather notifications
    weather_alerts = models.BooleanField(default=True)
    extreme_weather_warnings = models.BooleanField(default=True)
    disease_risk_alerts = models.BooleanField(default=True)

    # Disease notifications
    disease_detection_alerts = models.BooleanField(default=True)
    treatment_reminders = models.BooleanField(default=True)

    # Market notifications
    market_price_alerts = models.BooleanField(default=False)
    product_availability_alerts = models.BooleanField(default=False)

    # System notifications
    system_updates = models.BooleanField(default=True)
    security_alerts = models.BooleanField(default=True)

    # Delivery preferences
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    sms_notifications = models.BooleanField(default=False)

    # Quiet hours
    quiet_hours_start = models.TimeField(blank=True, null=True)
    quiet_hours_end = models.TimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notification preferences for {self.user.username}"

    class Meta:
        verbose_name = "Notification Preference"
        verbose_name_plural = "Notification Preferences"