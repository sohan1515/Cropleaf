import os
import django
import random
from datetime import datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CropLeaf.settings')
django.setup()

from app.models import MandiLocation, MarketplaceProduct, User

def create_sample_marketplace_data():
    # Create sample mandi locations
    mandis_data = [
        {
            'name': 'Azadpur Mandi',
            'district': 'North Delhi',
            'state': 'Delhi',
            'latitude': 28.7071,
            'longitude': 77.1707,
            'address': 'Azadpur, Delhi',
            'contact_number': '+91-9876543210',
            'operating_hours': '4:00 AM - 12:00 PM',
            'facilities': ['Cold Storage', 'Weighing Machines', 'Parking']
        },
        {
            'name': 'Lasalgaon Mandi',
            'district': 'Nashik',
            'state': 'Maharashtra',
            'latitude': 20.1427,
            'longitude': 74.2421,
            'address': 'Lasalgaon, Nashik, Maharashtra',
            'contact_number': '+91-9876543211',
            'operating_hours': '5:00 AM - 2:00 PM',
            'facilities': ['Cold Storage', 'Quality Testing Lab', 'Parking', 'Rest Rooms']
        },
        {
            'name': 'Vashi Mandi',
            'district': 'Thane',
            'state': 'Maharashtra',
            'latitude': 19.0771,
            'longitude': 73.0176,
            'address': 'Vashi, Navi Mumbai, Maharashtra',
            'contact_number': '+91-9876543212',
            'operating_hours': '6:00 AM - 4:00 PM',
            'facilities': ['Modern Storage', 'Quality Testing', 'E-commerce Platform']
        },
        {
            'name': 'Bangalore Mandi',
            'district': 'Bangalore Rural',
            'state': 'Karnataka',
            'latitude': 12.9716,
            'longitude': 77.5946,
            'address': 'Yeshwanthpur, Bangalore, Karnataka',
            'contact_number': '+91-9876543213',
            'operating_hours': '5:00 AM - 3:00 PM',
            'facilities': ['Cold Storage', 'Quality Lab', 'Online Trading Platform']
        },
        {
            'name': 'Pune Mandi',
            'district': 'Pune',
            'state': 'Maharashtra',
            'latitude': 18.5204,
            'longitude': 73.8567,
            'address': 'Pune, Maharashtra',
            'contact_number': '+91-9876543214',
            'operating_hours': '4:00 AM - 1:00 PM',
            'facilities': ['Storage Facilities', 'Quality Testing', 'Transportation']
        },
        {
            'name': 'Mumbai Mandi',
            'district': 'Mumbai Suburban',
            'state': 'Maharashtra',
            'latitude': 19.0760,
            'longitude': 72.8777,
            'address': 'Crawford Market, Mumbai, Maharashtra',
            'contact_number': '+91-9876543215',
            'operating_hours': '5:00 AM - 2:00 PM',
            'facilities': ['Historic Market', 'Quality Control', 'Transportation']
        },
        {
            'name': 'Chennai Mandi',
            'district': 'Chennai',
            'state': 'Tamil Nadu',
            'latitude': 13.0827,
            'longitude': 80.2707,
            'address': 'Koyambedu Market, Chennai, Tamil Nadu',
            'contact_number': '+91-9876543216',
            'operating_hours': '4:00 AM - 12:00 PM',
            'facilities': ['Large Capacity', 'Cold Storage', 'Quality Testing']
        },
        {
            'name': 'Kolkata Mandi',
            'district': 'Kolkata',
            'state': 'West Bengal',
            'latitude': 22.5726,
            'longitude': 88.3639,
            'address': 'Horticultural Market, Kolkata, West Bengal',
            'contact_number': '+91-9876543217',
            'operating_hours': '5:30 AM - 1:30 PM',
            'facilities': ['Regional Hub', 'Cold Storage', 'Logistics']
        },
        {
            'name': 'Hyderabad Mandi',
            'district': 'Hyderabad',
            'state': 'Telangana',
            'latitude': 17.3850,
            'longitude': 78.4867,
            'address': 'Kothapet Market, Hyderabad, Telangana',
            'contact_number': '+91-9876543218',
            'operating_hours': '5:00 AM - 1:00 PM',
            'facilities': ['Modern Infrastructure', 'Quality Control', 'E-commerce']
        },
        {
            'name': 'Ahmedabad Mandi',
            'district': 'Ahmedabad',
            'state': 'Gujarat',
            'latitude': 23.0225,
            'longitude': 72.5714,
            'address': 'Dudheshwar Mandi, Ahmedabad, Gujarat',
            'contact_number': '+91-9876543219',
            'operating_hours': '4:30 AM - 12:30 PM',
            'facilities': ['Cotton Trading', 'Quality Testing', 'Warehousing']
        },
        {
            'name': 'Jaipur Mandi',
            'district': 'Jaipur',
            'state': 'Rajasthan',
            'latitude': 26.9124,
            'longitude': 75.7873,
            'address': 'Sanganer Mandi, Jaipur, Rajasthan',
            'contact_number': '+91-9876543220',
            'operating_hours': '5:00 AM - 2:00 PM',
            'facilities': ['Spice Market', 'Cold Storage', 'Transportation']
        },
        {
            'name': 'Lucknow Mandi',
            'district': 'Lucknow',
            'state': 'Uttar Pradesh',
            'latitude': 26.8467,
            'longitude': 80.9462,
            'address': 'Aminabad Mandi, Lucknow, Uttar Pradesh',
            'contact_number': '+91-9876543221',
            'operating_hours': '5:30 AM - 1:30 PM',
            'facilities': ['Regional Market', 'Quality Control', 'Logistics']
        },
        {
            'name': 'Patna Mandi',
            'district': 'Patna',
            'state': 'Bihar',
            'latitude': 25.5941,
            'longitude': 85.1376,
            'address': 'Khajpura Mandi, Patna, Bihar',
            'contact_number': '+91-9876543222',
            'operating_hours': '5:00 AM - 1:00 PM',
            'facilities': ['Grain Storage', 'Quality Testing', 'Transportation']
        },
        {
            'name': 'Bhopal Mandi',
            'district': 'Bhopal',
            'state': 'Madhya Pradesh',
            'latitude': 23.2599,
            'longitude': 77.4126,
            'address': 'Shakti Nagar Mandi, Bhopal, Madhya Pradesh',
            'contact_number': '+91-9876543223',
            'operating_hours': '5:30 AM - 2:30 PM',
            'facilities': ['Modern Facilities', 'Cold Storage', 'E-auction']
        }
    ]

    mandis = []
    for mandi_data in mandis_data:
        mandi, created = MandiLocation.objects.get_or_create(
            name=mandi_data['name'],
            defaults=mandi_data
        )
        mandis.append(mandi)
        if created:
            print(f"Created mandi: {mandi.name}")

    # Get existing users or create sample ones
    users = list(User.objects.all())
    if not users:
        for i in range(3):
            user, created = User.objects.get_or_create(
                username=f'seller{i+1}',
                defaults={
                    'email': f'seller{i+1}@example.com',
                    'first_name': f'Seller {i+1}',
                    'is_active': True
                }
            )
            if created:
                user.set_password('password123')
                user.save()
            users.append(user)

    # Create sample products
    products_data = [
        {
            'title': 'Premium Quality Tomatoes',
            'description': 'Fresh, organic tomatoes grown without pesticides. Perfect for retail and wholesale buyers.',
            'product_type': 'crop',
            'category': 'Vegetables',
            'quantity': 500,
            'unit': 'kg',
            'price_per_unit': 45.00,
            'location': 'Nashik, Maharashtra',
            'latitude': 19.9975,
            'longitude': 73.7898,
            'quality_grade': 'a',
            'ai_verified': True,
            'ai_confidence_score': 0.95,
            'images': ['/static/images/crops/tomatoes_1.jpg', '/static/images/crops/tomatoes_2.jpg']
        },
        {
            'title': 'Certified Rice Seeds',
            'description': 'High-yielding rice seeds with excellent germination rate. Suitable for commercial farming.',
            'product_type': 'seed',
            'category': 'Seeds',
            'quantity': 1000,
            'unit': 'kg',
            'price_per_unit': 120.00,
            'location': 'Pune, Maharashtra',
            'latitude': 18.5204,
            'longitude': 73.8567,
            'quality_grade': 'a',
            'ai_verified': True,
            'ai_confidence_score': 0.92,
            'images': ['/static/images/crops/rice_seeds.jpg']
        },
        {
            'title': 'Fresh Corn Cobs',
            'description': 'Sweet corn harvested at peak freshness. Ideal for direct consumption and processing.',
            'product_type': 'crop',
            'category': 'Vegetables',
            'quantity': 300,
            'unit': 'kg',
            'price_per_unit': 25.00,
            'location': 'Aurangabad, Maharashtra',
            'latitude': 19.8762,
            'longitude': 75.3433,
            'quality_grade': 'b',
            'ai_verified': True,
            'ai_confidence_score': 0.88,
            'images': ['/static/images/crops/corn.jpg']
        },
        {
            'title': 'Organic Potato Seeds',
            'description': 'Disease-resistant potato seeds for healthy crop production.',
            'product_type': 'seed',
            'category': 'Seeds',
            'quantity': 800,
            'unit': 'kg',
            'price_per_unit': 85.00,
            'location': 'Bangalore, Karnataka',
            'latitude': 12.9716,
            'longitude': 77.5946,
            'quality_grade': 'a',
            'ai_verified': True,
            'ai_confidence_score': 0.94,
            'images': ['/static/images/crops/potato_seeds.jpg']
        },
        {
            'title': 'Premium Wheat Grains',
            'description': 'High-protein wheat grains suitable for flour milling and food processing.',
            'product_type': 'crop',
            'category': 'Grains',
            'quantity': 2000,
            'unit': 'kg',
            'price_per_unit': 35.00,
            'location': 'Delhi',
            'latitude': 28.7041,
            'longitude': 77.1025,
            'quality_grade': 'a',
            'ai_verified': True,
            'ai_confidence_score': 0.96,
            'images': ['/static/images/crops/wheat.jpg']
        }
    ]

    for i, product_data in enumerate(products_data):
        seller = random.choice(users)
        nearest_mandi = random.choice(mandis)

        product, created = MarketplaceProduct.objects.get_or_create(
            title=product_data['title'],
            seller=seller,
            defaults={
                **product_data,
                'nearest_mandi': nearest_mandi
            }
        )

        if created:
            print(f"Created product: {product.title}")

    print("Sample marketplace data created successfully!")
    print(f"Created {MandiLocation.objects.count()} mandis")
    print(f"Created {MarketplaceProduct.objects.count()} products")

if __name__ == '__main__':
    create_sample_marketplace_data()