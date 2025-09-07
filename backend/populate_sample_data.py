import os
import django
import random
from datetime import datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CropLeaf.settings')
django.setup()

from app.models import Disease, PredictionHistory, User, FarmerProfile

def create_sample_data():
    # Get all diseases
    diseases = list(Disease.objects.all())
    if not diseases:
        print("No diseases found. Run populate_treatments first.")
        return

    # Create sample users if they don't exist
    users = []
    for i in range(5):
        username = f'farmer{i+1}'
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': f'{username}@example.com',
                'first_name': f'Farmer {i+1}',
                'is_active': True
            }
        )
        if created:
            user.set_password('password123')
            user.save()

        # Create farmer profile
        FarmerProfile.objects.get_or_create(
            user=user,
            defaults={
                'farm_name': f'Farm {i+1}',
                'location': random.choice(['Tamil Nadu', 'Karnataka', 'Maharashtra', 'Punjab', 'Haryana']),
                'farm_size': random.randint(5, 50),
                'primary_crops': random.sample(['Corn', 'Tomato', 'Potato', 'Rice', 'Wheat'], random.randint(1, 3))
            }
        )
        users.append(user)

    # Create sample predictions for the last 30 days
    locations = ['Tamil Nadu', 'Karnataka', 'Maharashtra', 'Punjab', 'Haryana', 'Rajasthan']
    crops = ['Corn', 'Tomato', 'Potato']

    for i in range(150):  # Create 150 sample predictions
        days_ago = random.randint(0, 29)
        created_date = datetime.now() - timedelta(days=days_ago)

        disease = random.choice(diseases)
        user = random.choice(users) if random.random() > 0.3 else None  # 70% have users

        PredictionHistory.objects.create(
            user=user,
            disease=disease,
            confidence_score=random.uniform(0.5, 0.95),
            location=random.choice(locations),
            crop_type=random.choice(crops),
            created_at=created_date
        )

    print("Sample data created successfully!")
    print(f"Created {PredictionHistory.objects.count()} predictions")

if __name__ == '__main__':
    create_sample_data()