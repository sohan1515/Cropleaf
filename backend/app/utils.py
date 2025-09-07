import uuid
import numpy as np
from PIL import Image 
from functools import wraps
from app.model import model
from django.shortcuts import redirect
from django.core.files.storage import default_storage

def anonymous_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return view_func(request, *args, **kwargs)
    return wrapper


disease_class = [
        'Cercospora Leaf Spot',
        'Corn Common rust',
        'Corn Northern Leaf Blight',
        'Corn healthy',
        'Early Blight in Potatoes',
        'Late Blight in Potatoes',
        'Potato healthy',
        'Bacterial Spot in Tomatoes',
        'Tomato Early blight',
        'Tomato Late blight',
        'Tomato Leaf Mold',
        'Tomato Septoria leaf spot',
        'Tomato Spider mites two spotted spider mite',
        'Tomato Target Spot',
        'Tomato Yellow Leaf Curl Virus',
        'Tomato mosaic virus',
        'Tomato healthy'
]


crop = [
            {   # 00
                'image_path': 'images/crops/Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot.jpeg',
                'crop_id': '0',
                'title': 'Cercospora Leaf Spot',
                'description': 'Cercospora leaf spot, or gray leaf spot (GLS), is a fungal disease in corn caused by Cercospora zeaemaydis. It spreads through spores in warm, humid conditions, causing gray to tan lesions on leaves. This reduces photosynthesis and lowers yields. Management includes resistant hybrids, crop rotation, residue removal, and fungicides to prevent severe infections and yield loss.'
            },

            {   # 01
                'image_path': 'images/crops/Corn_(maize)___Common_rust.jpeg',
                'crop_id': '1',
                'title': 'Corn Common rust',
                'description': 'Common rust in corn (maize) is a fungal disease caused by Puccinia sorghi. It thrives in cool, humid conditions and spreads through windborne spores. Symptoms include reddish-brown pustules on leaves, which can merge and weaken the plant, reducing photosynthesis and yield. Management includes planting resistant hybrids, crop rotation, and timely fungicide applications in severe cases.'
            },

            {   # 02
                'image_path': 'images/crops/Corn_(maize)___Northern_Leaf_Blight.jpeg',
                'crop_id': '2',
                'title': 'Corn Northern Leaf Blight',
                'description': 'Northern Leaf Blight (NLB) in corn is caused by Exserohilum turcicum and thrives in cool, humid conditions. It causes long, grayish-green, cigarshaped lesions on leaves, reducing photosynthesis and yield. The disease spreads through windborne spores. Management includes resistant hybrids, crop rotation, residue reduction, and fungicide application in severe cases to prevent major yield loss.'
            },

            {   # 04
                'image_path': 'images/crops/Potato___Early_blight.jpeg',
                'crop_id': '4',
                'title': 'Early Blight in Potatoes',
                'description': 'Early blight in potatoes is a fungal disease caused by Alternaria solani. It thrives in warm, humid conditionsand spreads through spores in soil and plant debris. Symptoms include dark brown spots with concentric rings on lower leaves, leading to defoliation and reduced yield. Management includes crop rotation, resistant varieties, proper irrigation, and fungicide application in severe cases.'
            },

            {   # 05
                'image_path': 'images/crops/Potato___Late_blight.jpeg',
                'crop_id': '5',
                'title': 'Late Blight in Potatoes',
                'description': 'The disease can destroy foliage, stems, and tubers, leading to significant yield Late blight in potatoes is a devastating fungal-like disease caused by Phytophthora infestans. It thrives in cool, wet conditions and spreads rapidly through airborne spores. Symptoms include water-soaked lesions on leaves, which turn brown and spread quickly, leading to plant decay. Management includes resistant varieties, proper spacing, crop rotation, and fungicide application to prevent severe yield loss.'
            },

            {   # 07
                'image_path': 'images/crops/Tomato___Bacterial_spot.jpeg',
                'crop_id': '7',
                'title': 'Bacterial Spot in Tomatoes',
                'description': 'Bacterial spot in tomatoes is caused by Xanthomonas species and thrives in warm, humid conditions. It spreads through infected seeds, plant debris, and water splashes. Symptoms include small, dark, water-soaked spots on leaves and fruits, leading to defoliation and reduced yield. Management includes using resistant varieties, certified disease-free seeds, crop rotation, and copper-based bactericides.'
            },

            {   # 08
                'image_path': 'images/crops/Tomato___Early_blight.jpeg',
                'crop_id': '8',
                'title': 'Tomato Early blight',
                'description': 'Early blight in tomatoes is caused by Alternaria solani and thrives in warm, humid conditions. It spreads through soil, water splashes, and infected plant debris. Symptoms include dark, concentricringed spots on lower leaves, leading to yellowing and defoliation. Management includes using resistant varieties, crop rotation, proper spacing, mulching, and fungicide application in severe cases.'
            },

            {   # 09
                'image_path': 'images/crops/Tomato___late_blight.jpeg',
                'crop_id': '9',
                'title': 'Tomato late blight',
                'description': 'Late blight in tomatoes is caused by Phytophthora infestans and thrives in cool, wet conditions. It spreads rapidly through windborne spores, causing watersoaked lesions on leaves that turn brown and spread quickly. Infected fruits develop dark, firm rot. Management includes resistant varieties, proper spacing, avoiding overhead watering, crop rotation, and fungicide application to prevent severe losses.'
            },

            {   # 10
                'image_path': 'images/crops/Tomato___Leaf_Mold.jpeg',
                'crop_id': '10',
                'title': 'Tomato Leaf Mold',
                'description': 'Tomato leaf mold is caused by Passalora fulva and thrives in warm, humid conditions. It spreads through airborne spores, affecting mainly greenhouse and densely planted crops. Symptoms include yellow spots on upper leaves and velvety olive-green mold on the undersides, leading to defoliation and reduced yield. Management includes proper ventilation, resistant varieties, crop rotation, and fungicide application when necessary.'
            },

            {   # 11
                'image_path': 'images/crops/Tomato___Septoria_leaf_spot.jpeg',
                'crop_id': '11',
                'title': 'Tomato Septoria leaf spot',
                'description': 'Septoria leaf spot in tomatoes is caused by Septoria lycopersici and thrives in warm, humid conditions. It spreads through water splashes and infected plant debris. Symptoms include small, circular spots with dark edges and gray centers on lower leaves, leading to defoliation and reduced yield. Management includes resistant varieties, proper spacing, crop rotation, and fungicide application when necessary.'
            },

            {   # 12
                'image_path': 'images/crops/Tomato_Spider_mites_two_ spotted_spider_mite.jpeg',
                'crop_id': '12',
                'title': 'Tomato Spider mites two spotted spider mite',
                'description': 'Two-spotted spider mites (Tetranychus urticae) are tiny pests that attack tomato plants, thriving in hot, dry conditions. They feed on leaf sap, causing yellowing, speckling, and eventual leaf drop. Severe infestations lead to webbing on leaves and stems. Management includes regular watering, introducing natural predators (like ladybugs), insecticidal soaps, neem oil, and removing heavily infested leaves.'
            },

            {   # 13
                'image_path': 'images/crops/Tomato___Target_Spot.jpeg',
                'crop_id': '13',
                'title': 'Tomato Target Spot',
                'description': 'Target spot in tomatoes is caused by Corynespora cassiicola and thrives in warm, humid conditions. It spreads through water splashes, wind, and infected plant debris. Symptoms include brown, circular leaf spots with concentric rings, leading to defoliation and reduced yield. Management includes crop rotation, resistant varieties, proper spacing, and fungicide application when necessary.'
            },

            {   # 14
                'image_path': 'images/crops/Tomato___Tomato_Yellow_Leaf_Curl_Virus.jpeg',
                'crop_id': '14',
                'title': 'Tomato Tomato Yellow Leaf Curl Virus',
                'description': 'Tomato Yellow Leaf Curl Virus (TYLCV) is a viral disease transmitted by whiteflies (Bemisia tabaci). It causes yellowing, curling of leaves, stunted growth, and reduced fruit production. The virus spreads rapidly in warm conditions. Management includes planting resistant varieties, controlling whiteflies with insecticides or natural predators, using reflective mulches, and removing infected plants to prevent further spread.'
            },

            {   # 15
                'image_path': 'images/crops/Tomato___Tomato_mosaic_virus.jpeg',
                'crop_id': '15',
                'title': 'Tomato Tomato mosaic virus',
                'description': 'Tomato mosaic virus (ToMV) is a highly contagious viral disease that spreads through contaminated tools, hands, seeds, and plant debris. Symptoms include mottled, curled, and deformed leaves, stunted growth, and reduced fruit quality with internal browning. Management includes using resistant varieties, disinfecting tools, avoiding tobacco exposure, removing infected plants, and practicing crop rotation to prevent further spread.'
            },

]



developers = [

           {
              'name':'Yash Chavan',
              'linkedin' : 'https://www.linkedin.com/in/yashchavan02/'
           },

           {
              'name':'Ranjit Chavan',
              'linkedin' : 'https://www.linkedin.com/in/ranjit-chavan-073613291/'
           },

           {
              'name':'Prathamesh Doiphode',
              'linkedin' : 'https://www.linkedin.com/in/ranjit-chavan-073613291/'
           },

           {
              'name':'Sudarshan Gaikwad',
              'linkedin' : 'https://www.linkedin.com/in/ranjit-chavan-073613291/'
           },

]

small_image_size = """
                <html>
                    <head>
                        <title>CropLeaf | Valid Image</title>
                        <style>
                            body {
                                display: flex;
                                justify-content: center;
                                align-items: center;
                                height: 100vh;
                                margin: 0;
                                font-family: Arial, sans-serif;
                                background-color: #f9f9f9;
                                text-align: center;
                                user-select: none;
                                -webkit-user-select: none;
                                -moz-user-select: none;
                                -ms-user-select: none;
                            }
                        </style>
                    </head>
                    <body>
                        <div>
                            <h1>To ensure accurate results, please upload an image with higher resolution.</h1>
                        </div>
                    </body>
                </html>
                """


under_maintenance = """
                <html>
                    <head>
                        <title>CropLeaf | Maintenance</title>
                        <style>
                            body {
                                display: flex;
                                justify-content: center;
                                align-items: center;
                                height: 100vh;
                                margin: 0;
                                font-family: Arial, sans-serif;
                                background-color: #f9f9f9;
                                text-align: center;
                                user-select: none;
                                -webkit-user-select: none;
                                -moz-user-select: none;
                                -ms-user-select: none;
                            }
                        </style>
                    </head>
                    <body>
                        <div>
                            <h1>We'll Be Right Back</h1>
                            <h3>Our website is currently undergoing scheduled maintenance to improve your experience.</h3>
                        </div>
                    </body>
                </html>
                """


def process_image(full_path):
    if full_path.lower().endswith(".svg"):
        raise ValueError("SVG files are not supported.")

    image = Image.open(full_path).convert("RGB")
    image_resized = image.resize((256, 256), Image.LANCZOS)

    compressed_filename = f"{uuid.uuid4()}.webp"
    compressed_path = default_storage.path(compressed_filename)
    image_resized.save(compressed_path, format="WebP", lossless=True)

    image_array = np.expand_dims(np.array(image_resized), axis=0)

    # Check if model is available
    if model.model_type is None:
        return "Model not available. Please check model loading.", [full_path, compressed_path]

    try:
        prediction = model.predict(image_array)

        # Handle different output formats
        if isinstance(prediction, np.ndarray):
            if len(prediction.shape) > 1:
                pred_index = np.argmax(prediction)
                max_probability = prediction[0][pred_index] if len(prediction.shape) > 1 else prediction[pred_index]
            else:
                pred_index = np.argmax(prediction)
                max_probability = prediction[pred_index]
        else:
            # Handle PyTorch tensor output
            prediction = prediction.detach().numpy() if hasattr(prediction, 'detach') else np.array(prediction)
            pred_index = np.argmax(prediction)
            max_probability = prediction[0][pred_index] if len(prediction.shape) > 1 else prediction[pred_index]

        result = (
            "Provided image doesn’t seem to be a crop leaf."
            if max_probability < 0.5
            else disease_class[pred_index]
            if pred_index < len(disease_class)
            else "Provided image doesn’t seem to be a crop leaf."
        )

    except Exception as e:
        print(f"Prediction error: {str(e)}")
        result = "Error processing image with model."

    return result, max_probability, [full_path, compressed_path]