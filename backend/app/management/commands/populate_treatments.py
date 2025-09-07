from django.core.management.base import BaseCommand
from app.models import Disease, Treatment, PreventionStrategy

class Command(BaseCommand):
    help = 'Populate database with disease treatments and prevention strategies'

    def handle(self, *args, **options):
        self.stdout.write('Populating treatment database...')

        # Disease data mapping with comprehensive information
        disease_data = {
            'Cercospora Leaf Spot': {
                'scientific_name': 'Cercospora zeae-maydis',
                'description': 'Fungal disease causing gray to tan lesions on corn leaves, also known as gray leaf spot. It is one of the most destructive diseases of corn worldwide.',
                'affected_crops': ['Corn', 'Maize'],
                'severity_levels': {'mild': 'Small lesions on lower leaves', 'moderate': 'Multiple lesions on middle leaves', 'severe': 'Heavy defoliation affecting yield'},
                'symptoms': ['Gray lesions with tan centers', 'Rectangular lesions parallel to leaf veins', 'Leaf yellowing and death'],
                'causal_agent': 'Fungus - Cercospora zeae-maydis',
                'host_range': 'Primarily corn (Zea mays), occasionally other grasses',
                'environmental_conditions': 'High humidity (>85%), temperatures 20-30°C, extended leaf wetness periods',
                'disease_cycle': 'Overwinters in corn residue, spores released during rain, infection occurs through stomata',
                'economic_impact': 'Can cause 30-50% yield loss in severe cases, especially in continuous corn production',
                'cultural_control': 'Crop rotation (2-3 years out of corn), residue management, resistant hybrids, proper plant spacing',
                'chemical_control': 'Fungicides: azoxystrobin, pyraclostrobin, trifloxystrobin. Apply at tasseling and 7-10 days later',
                'biological_control': 'Limited options, focus on cultural practices',
                'integrated_management': 'Use resistant varieties + fungicides only when needed + proper residue management',
                'references': 'University of Nebraska Extension, Iowa State University Plant Pathology',
                'prevention_priority': 'high'
            },
            'Corn Common rust': {
                'scientific_name': 'Puccinia sorghi',
                'description': 'Fungal disease causing reddish-brown pustules on corn leaves. One of the most common and widespread diseases of corn worldwide.',
                'affected_crops': ['Corn', 'Maize', 'Sweet corn'],
                'severity_levels': {'mild': 'Few pustules on lower leaves', 'moderate': 'Pustules on middle leaves', 'severe': 'Heavy infection affecting photosynthesis'},
                'symptoms': ['Reddish-brown elliptical pustules', 'Pustules rupture releasing orange spores', 'Premature leaf death'],
                'causal_agent': 'Fungus - Puccinia sorghi',
                'host_range': 'Corn (Zea mays), teosinte, and some wild grasses',
                'environmental_conditions': 'Cool temperatures (15-25°C), high humidity, dew formation',
                'disease_cycle': 'Overwinters in southern regions, spreads via wind-borne spores, multiple infection cycles per season',
                'economic_impact': 'Yield losses up to 20-40% in susceptible varieties, reduced grain quality',
                'cultural_control': 'Plant resistant varieties, avoid late planting, proper plant spacing for air circulation',
                'chemical_control': 'Fungicides: azoxystrobin, pyraclostrobin when pustules first appear',
                'biological_control': 'Limited, focus on resistant varieties',
                'integrated_management': 'Use resistant hybrids + monitor weather conditions + timely fungicide application',
                'references': 'Cornell University Extension, University of Wisconsin Extension',
                'prevention_priority': 'moderate'
            },
            'Corn Northern Leaf Blight': {
                'scientific_name': 'Exserohilum turcicum',
                'description': 'Fungal disease causing long cigar-shaped lesions on corn leaves',
                'affected_crops': ['Corn', 'Maize'],
                'severity_levels': {'mild': 'Small lesions', 'moderate': 'Long lesions', 'severe': 'Complete defoliation'},
                'symptoms': ['Cigar-shaped lesions', 'Gray-green discoloration', 'Yield loss']
            },
            'Early Blight in Potatoes': {
                'scientific_name': 'Alternaria solani',
                'description': 'Fungal disease causing dark spots with concentric rings on potato leaves',
                'affected_crops': ['Potato'],
                'severity_levels': {'mild': 'Few spots', 'moderate': 'Multiple spots', 'severe': 'Defoliation'},
                'symptoms': ['Dark spots', 'Concentric rings', 'Leaf death']
            },
            'Late Blight in Potatoes': {
                'scientific_name': 'Phytophthora infestans',
                'description': 'Devastating fungal disease causing water-soaked lesions on potato plants',
                'affected_crops': ['Potato'],
                'severity_levels': {'mild': 'Small lesions', 'moderate': 'Spreading lesions', 'severe': 'Plant death'},
                'symptoms': ['Water-soaked lesions', 'White mold', 'Rapid spread']
            },
            'Bacterial Spot in Tomatoes': {
                'scientific_name': 'Xanthomonas spp.',
                'description': 'Bacterial disease causing small dark spots on tomato leaves and fruits',
                'affected_crops': ['Tomato'],
                'severity_levels': {'mild': 'Few spots', 'moderate': 'Many spots', 'severe': 'Fruit damage'},
                'symptoms': ['Small dark spots', 'Leaf spots', 'Fruit lesions']
            },
            'Tomato Early blight': {
                'scientific_name': 'Alternaria solani',
                'description': 'Fungal disease causing dark spots on tomato leaves',
                'affected_crops': ['Tomato'],
                'severity_levels': {'mild': 'Small spots', 'moderate': 'Large spots', 'severe': 'Defoliation'},
                'symptoms': ['Dark spots', 'Yellow halos', 'Leaf drop']
            },
            'Tomato Late blight': {
                'scientific_name': 'Phytophthora infestans',
                'description': 'Destructive fungal disease causing rapid plant decay',
                'affected_crops': ['Tomato'],
                'severity_levels': {'mild': 'Small lesions', 'moderate': 'Spreading decay', 'severe': 'Plant death'},
                'symptoms': ['Water-soaked lesions', 'White mold', 'Rapid death']
            },
            'Tomato Leaf Mold': {
                'scientific_name': 'Passalora fulva',
                'description': 'Fungal disease causing yellow spots and mold on tomato leaves',
                'affected_crops': ['Tomato'],
                'severity_levels': {'mild': 'Few spots', 'moderate': 'Mold growth', 'severe': 'Heavy defoliation'},
                'symptoms': ['Yellow spots', 'Velvety mold', 'Leaf curling']
            },
            'Tomato Septoria leaf spot': {
                'scientific_name': 'Septoria lycopersici',
                'description': 'Fungal disease causing small circular spots on tomato leaves',
                'affected_crops': ['Tomato'],
                'severity_levels': {'mild': 'Small spots', 'moderate': 'Many spots', 'severe': 'Defoliation'},
                'symptoms': ['Small circular spots', 'Dark edges', 'Gray centers']
            },
            'Tomato Target Spot': {
                'scientific_name': 'Corynespora cassiicola',
                'description': 'Fungal disease causing brown spots with concentric rings on tomato leaves',
                'affected_crops': ['Tomato'],
                'severity_levels': {'mild': 'Few spots', 'moderate': 'Multiple spots', 'severe': 'Defoliation'},
                'symptoms': ['Brown spots', 'Concentric rings', 'Leaf yellowing']
            },
            'Tomato Yellow Leaf Curl Virus': {
                'scientific_name': 'TYLCV',
                'description': 'Viral disease transmitted by whiteflies causing leaf curling and yellowing',
                'affected_crops': ['Tomato'],
                'severity_levels': {'mild': 'Mild curling', 'moderate': 'Severe curling', 'severe': 'Stunted growth'},
                'symptoms': ['Leaf curling', 'Yellowing', 'Stunted growth']
            },
            'Tomato mosaic virus': {
                'scientific_name': 'ToMV',
                'description': 'Viral disease causing mottled leaves and reduced fruit quality',
                'affected_crops': ['Tomato'],
                'severity_levels': {'mild': 'Light mottling', 'moderate': 'Heavy mottling', 'severe': 'Fruit damage'},
                'symptoms': ['Mottled leaves', 'Distorted growth', 'Reduced yield']
            }
        }

        # Create diseases with comprehensive information
        for disease_name, data in disease_data.items():
            disease, created = Disease.objects.get_or_create(
                name=disease_name,
                defaults={
                    'scientific_name': data['scientific_name'],
                    'description': data['description'],
                    'affected_crops': data['affected_crops'],
                    'severity_levels': data['severity_levels'],
                    'symptoms': data['symptoms'],
                    'causal_agent': data.get('causal_agent', ''),
                    'host_range': data.get('host_range', ''),
                    'environmental_conditions': data.get('environmental_conditions', ''),
                    'disease_cycle': data.get('disease_cycle', ''),
                    'economic_impact': data.get('economic_impact', ''),
                    'cultural_control': data.get('cultural_control', ''),
                    'chemical_control': data.get('chemical_control', ''),
                    'biological_control': data.get('biological_control', ''),
                    'integrated_management': data.get('integrated_management', ''),
                    'references': data.get('references', ''),
                    'prevention_priority': data.get('prevention_priority', 'moderate')
                }
            )
            if created:
                self.stdout.write(f'Created disease: {disease_name}')
            else:
                # Update existing disease with new comprehensive information
                for field, value in data.items():
                    if hasattr(disease, field) and getattr(disease, field) != value:
                        setattr(disease, field, value)
                disease.save()
                self.stdout.write(f'Updated disease: {disease_name}')

        # Treatment data
        treatment_data = [
            # Corn diseases treatments
            {
                'disease': 'Cercospora Leaf Spot',
                'name': 'Fungicide Application (Chemical)',
                'description': 'Apply fungicides containing azoxystrobin or pyraclostrobin',
                'treatment_type': 'chemical',
                'effectiveness_rating': 4,
                'application_method': 'Spray every 7-10 days during humid conditions',
                'safety_precautions': 'Wear protective clothing, avoid spraying near water sources',
                'cost_estimate': 25.00,
                'duration_days': 7
            },
            {
                'disease': 'Cercospora Leaf Spot',
                'name': 'Crop Rotation (Cultural)',
                'description': 'Rotate corn with non-host crops like soybeans or wheat',
                'treatment_type': 'cultural',
                'effectiveness_rating': 3,
                'application_method': 'Plan crop rotation for 2-3 year cycles',
                'safety_precautions': 'None',
                'cost_estimate': 0.00,
                'duration_days': 365
            },
            {
                'disease': 'Corn Common rust',
                'name': 'Rust-Resistant Varieties',
                'description': 'Plant rust-resistant corn hybrids',
                'treatment_type': 'preventive',
                'effectiveness_rating': 5,
                'application_method': 'Select resistant varieties when planting',
                'safety_precautions': 'None',
                'cost_estimate': 5.00,
                'duration_days': 120
            },
            {
                'disease': 'Corn Northern Leaf Blight',
                'name': 'Fungicide Spray Program',
                'description': 'Apply fungicides at tasseling and 7-10 days later',
                'treatment_type': 'chemical',
                'effectiveness_rating': 4,
                'application_method': 'Two applications: at tasseling and 7-10 days later',
                'safety_precautions': 'Follow label instructions, wear PPE',
                'cost_estimate': 30.00,
                'duration_days': 10
            },
            # Potato diseases treatments
            {
                'disease': 'Early Blight in Potatoes',
                'name': 'Chlorothalonil Fungicide',
                'description': 'Apply chlorothalonil-based fungicides every 7-10 days',
                'treatment_type': 'chemical',
                'effectiveness_rating': 4,
                'application_method': 'Spray every 7-10 days starting at first sign of disease',
                'safety_precautions': 'Wear protective gear, follow re-entry intervals',
                'cost_estimate': 20.00,
                'duration_days': 7
            },
            {
                'disease': 'Late Blight in Potatoes',
                'name': 'Systemic Fungicide Treatment',
                'description': 'Apply systemic fungicides like mefenoxam',
                'treatment_type': 'chemical',
                'effectiveness_rating': 5,
                'application_method': 'Apply at first sign of disease, repeat every 7 days',
                'safety_precautions': 'Use according to label, protect water sources',
                'cost_estimate': 35.00,
                'duration_days': 3
            },
            # Tomato diseases treatments
            {
                'disease': 'Bacterial Spot in Tomatoes',
                'name': 'Copper-Based Bactericide',
                'description': 'Apply copper hydroxide or copper sulfate sprays',
                'treatment_type': 'chemical',
                'effectiveness_rating': 3,
                'application_method': 'Spray every 7-10 days, starting preventively',
                'safety_precautions': 'Avoid copper accumulation in soil',
                'cost_estimate': 15.00,
                'duration_days': 7
            },
            {
                'disease': 'Tomato Early blight',
                'name': 'Mancozeb Fungicide',
                'description': 'Apply mancozeb-based fungicides preventively',
                'treatment_type': 'chemical',
                'effectiveness_rating': 4,
                'application_method': 'Apply every 7-14 days during growing season',
                'safety_precautions': 'Follow label rates, wear protective clothing',
                'cost_estimate': 18.00,
                'duration_days': 7
            },
            {
                'disease': 'Tomato Late blight',
                'name': 'Protectant Fungicide Program',
                'description': 'Apply protectant fungicides like mancozeb or chlorothalonil',
                'treatment_type': 'chemical',
                'effectiveness_rating': 4,
                'application_method': 'Weekly applications during humid conditions',
                'safety_precautions': 'Rotate fungicide classes to prevent resistance',
                'cost_estimate': 25.00,
                'duration_days': 7
            },
            {
                'disease': 'Tomato Yellow Leaf Curl Virus',
                'name': 'Insecticide for Whitefly Control',
                'description': 'Apply insecticides to control whitefly vectors',
                'treatment_type': 'chemical',
                'effectiveness_rating': 3,
                'application_method': 'Target whitefly populations with systemic insecticides',
                'safety_precautions': 'Use selective insecticides to protect beneficial insects',
                'cost_estimate': 22.00,
                'duration_days': 14
            }
        ]

        # Create treatments
        for treatment_info in treatment_data:
            try:
                disease = Disease.objects.get(name=treatment_info['disease'])
                treatment, created = Treatment.objects.get_or_create(
                    disease=disease,
                    name=treatment_info['name'],
                    defaults={
                        'description': treatment_info['description'],
                        'treatment_type': treatment_info['treatment_type'],
                        'effectiveness_rating': treatment_info['effectiveness_rating'],
                        'application_method': treatment_info['application_method'],
                        'safety_precautions': treatment_info['safety_precautions'],
                        'cost_estimate': treatment_info['cost_estimate'],
                        'duration_days': treatment_info['duration_days']
                    }
                )
                if created:
                    self.stdout.write(f'Created treatment: {treatment_info["name"]} for {treatment_info["disease"]}')
            except Disease.DoesNotExist:
                self.stdout.write(f'Disease not found: {treatment_info["disease"]}')

        # Prevention strategies
        prevention_data = [
            {
                'disease': 'Cercospora Leaf Spot',
                'title': 'Residue Management',
                'description': 'Remove and destroy corn residue after harvest',
                'strategy_type': 'cultural',
                'implementation_steps': [
                    'Harvest corn completely',
                    'Remove all plant debris from field',
                    'Deep plow to bury residue',
                    'Avoid planting corn in same field consecutively'
                ],
                'expected_benefits': 'Reduces overwintering fungal spores by 70-80%',
                'difficulty_level': 'moderate',
                'cost_impact': 'low'
            },
            {
                'disease': 'Corn Common rust',
                'title': 'Resistant Variety Selection',
                'description': 'Choose corn varieties with rust resistance genes',
                'strategy_type': 'preventive',
                'implementation_steps': [
                    'Research local rust-resistant varieties',
                    'Check extension service recommendations',
                    'Purchase certified seed',
                    'Monitor for new rust races'
                ],
                'expected_benefits': 'Up to 90% reduction in rust incidence',
                'difficulty_level': 'easy',
                'cost_impact': 'medium'
            },
            {
                'disease': 'Early Blight in Potatoes',
                'title': 'Proper Plant Spacing',
                'description': 'Provide adequate air circulation between plants',
                'strategy_type': 'cultural',
                'implementation_steps': [
                    'Space plants 12-15 inches apart',
                    'Space rows 30-36 inches apart',
                    'Avoid overhead irrigation',
                    'Mulch around plants to reduce soil splash'
                ],
                'expected_benefits': 'Reduces humidity around plants, slowing disease spread',
                'difficulty_level': 'easy',
                'cost_impact': 'low'
            },
            {
                'disease': 'Tomato Late blight',
                'title': 'Greenhouse Ventilation',
                'description': 'Maintain proper ventilation to reduce humidity',
                'strategy_type': 'cultural',
                'implementation_steps': [
                    'Install proper ventilation systems',
                    'Monitor humidity levels (<85%)',
                    'Use fans for air circulation',
                    'Avoid planting too densely'
                ],
                'expected_benefits': 'Reduces conditions favorable for late blight development',
                'difficulty_level': 'moderate',
                'cost_impact': 'medium'
            }
        ]

        # Create prevention strategies
        for prevention_info in prevention_data:
            try:
                disease = Disease.objects.get(name=prevention_info['disease'])
                strategy, created = PreventionStrategy.objects.get_or_create(
                    disease=disease,
                    title=prevention_info['title'],
                    defaults={
                        'description': prevention_info['description'],
                        'strategy_type': prevention_info['strategy_type'],
                        'implementation_steps': prevention_info['implementation_steps'],
                        'expected_benefits': prevention_info['expected_benefits'],
                        'difficulty_level': prevention_info['difficulty_level'],
                        'cost_impact': prevention_info['cost_impact']
                    }
                )
                if created:
                    self.stdout.write(f'Created prevention strategy: {prevention_info["title"]} for {prevention_info["disease"]}')
            except Disease.DoesNotExist:
                self.stdout.write(f'Disease not found: {prevention_info["disease"]}')

        self.stdout.write(self.style.SUCCESS('Successfully populated treatment database!'))
        self.stdout.write(f'Diseases: {Disease.objects.count()}')
        self.stdout.write(f'Treatments: {Treatment.objects.count()}')
        self.stdout.write(f'Prevention Strategies: {PreventionStrategy.objects.count()}')