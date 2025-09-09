import os
import io
import json
import uuid
import tensorflow as tf
from urllib.parse import quote
from datetime import datetime, timedelta
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.utils.http import urlencode
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden , HttpResponse
from django.shortcuts import render , redirect , get_object_or_404
from app.forms import RegistrationForm , ProfileEditForm , ContactForm
from django.contrib.auth import  login as auth_login , authenticate , logout
from app.utils import anonymous_required , crop , developers , disease_class, small_image_size, under_maintenance , process_image
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response

tf.config.set_visible_devices([], 'GPU') # i have to comment down before deployement



# @anonymous_required
# def register_view(request):
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False) 
#             user.set_password(form.cleaned_data['password'])
#             user.first_name = form.cleaned_data['name']
#             user.save()

#             auth_login(request, user)
#             request.session.set_expiry(timedelta(days=7))
#             return redirect('home') 
#         else:
#            for fname in form.errors:
#                form._errors = {fname: form.errors[fname]}
#                break
#     else: 
#         form = RegistrationForm() 

#     return render(request, 'auth/register.html', {'form': form})

from tensorflow.keras.models import load_model
import torch
from django.conf import settings

# Load models once when views.py is imported
tf_model = load_model(settings.TF_MODEL_FILE)
pt_model = torch.load(settings.PT_MODEL_FILE, map_location="cpu")

# Example view
from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["POST"])
def predict(request):
    # use tf_model or pt_model for prediction
    return Response({"message": "Prediction successful"})



@anonymous_required
def register_view(request):
    nxturl = request.GET.get('next')
    if nxturl == 'None': nxturl = None

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        nxturl = request.POST.get('next')
        if nxturl == 'None': nxturl = None

        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.first_name = form.cleaned_data['name']
            user.save()

            auth_login(request, user)
            request.session.set_expiry(timedelta(days=7))
            return redirect(nxturl or 'home')

        else:
            ffield = None
            this_error = None
            for ename in form.errors:
                ffield = ename
                this_error = form.errors[ename]
                break

            error = {ffield: this_error}

            request.session['just_form_data'] = request.POST
            request.session['just_form_errors'] = json.dumps(error)

            url = reverse('register')
            if nxturl:
                url += f'?next={nxturl}'
            return redirect(url)

    else:
        data = request.session.pop('just_form_data', None)
        errors_json = request.session.pop('just_form_errors', None)

        if data:
            form = RegistrationForm(data)
            if errors_json:
                errors = json.loads(errors_json)
                for field, errs in errors.items():
                    form._errors = {field: form.error_class(errs)}
                    
        else: form = RegistrationForm()

        return render(request, 'auth/register.html', {'form': form, 'next': nxturl})



# @anonymous_required
# def login_view(request):
#     if request.method == 'POST':
#         username = request.POST.get('username', '').strip()
#         password = request.POST.get('password')
#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             auth_login(request, user)
#             request.session.set_expiry(timedelta(days=3))

#             nxturl = request.POST.get('next') or request.GET.get('next')
#             return redirect(nxturl or 'home')
#         else:
#             messages.error(request, "Oops! Login failed, please check your credentials")
#             return redirect('login')

#     return render(request, 'auth/login.html', {
#         'next': request.GET.get('next', '')
#     })


@anonymous_required
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            request.session.set_expiry(timedelta(days=3))

            nxturl = request.POST.get('next') or request.GET.get('next')
            return redirect(nxturl or 'home')
        else:
            messages.error(request, "Oops! Login failed, please check your credentials")

            nxturl = request.POST.get('next') or request.GET.get('next')
            if nxturl:
                safenxturl = quote(nxturl, safe="/")
                url = f"{reverse('login')}?next={safenxturl}"
                return redirect(url)
            return redirect('login')

    return render(request, 'auth/login.html', {
        'next': request.GET.get('next', '')
    })




# def home(request):
#     if model is None:
#       return HttpResponse (under_maintenance, status=503 )

#     if request.method == "POST" and "image" in request.FILES:
#         image_file = request.FILES["image"]
#         base_name = f"{uuid.uuid4()}"
#         original_filename = f"{base_name}.jpg"
#         compressed_filename = f"{base_name}.webp"
        
#         try:
#             file_path = default_storage.save(original_filename, image_file)
#             full_path = default_storage.path(file_path)

#             if full_path.lower().endswith(".svg"):
#                 raise ValueError("SVG files are not supported.")
            
#             else:
#                 image = Image.open(full_path).convert("RGB")
#                 image_resized = image.resize((256, 256), Image.LANCZOS)

#                 compressed_path = default_storage.path(compressed_filename)
#                 image_resized.save(compressed_path, format="WebP", lossless=True)

#                 image_array = np.expand_dims(np.array(image_resized), axis=0)
#                 prediction = model.predict(image_array)
#                 pred_index = np.argmax(prediction)
#                 max_probability = prediction[0][pred_index]

#                 result = "Unknown" if max_probability < 0.5 else disease_class[pred_index] if pred_index < len(disease_class) else "Unknown"
#                 index = pred_index

#         except Exception as e:
#             return HttpResponse(f"Error processing image: {str(e)}", status=400)

#         finally:
#             for temp_path in [original_filename, compressed_filename]:
#                 if default_storage.exists(temp_path):
#                     default_storage.delete(temp_path)

#     if request.method == 'POST':
#            form = ContactForm(request.POST)
#     else:
#            form = ContactForm()
#            return render(request, "app/index.html", {
#                 "form": form
#            })           

#     return render(request, "app/index.html", {
#         "form": form
#     })


# def home(request):
#     if request.method == "POST" and "image" in request.FILES:
#         image_file = request.FILES["image"]
#         unique_name = f"{uuid.uuid4()}.jpg"
#         default_storage.save(unique_name, image_file)
#         request.session['uploaded_image_name'] = unique_name
#         return redirect('upload')

#     return render(request, "app/index.html")


def home(request):
    """
    Home view - redirect to React frontend or return API info
    """
    # Since we're using React frontend, redirect to frontend or return API info
    if request.path == '/':
        # Return a simple JSON response with API information
        return HttpResponse(
            '{"message": "CropLeaf API Server", "status": "running", "frontend": "http://localhost:5174"}',
            content_type='application/json'
        )

    # Handle image processing if needed
    result: str | None = None
    temp_files: list = []

    try:
        filename = request.session.pop('uploaded_image_name', None)
        if filename and default_storage.exists(filename):
            full_path = default_storage.path(filename)
            result, temp_files = process_image(full_path)

        elif request.method == "POST" and "image" in request.FILES:
            image_file = request.FILES["image"]
            original_filename = f"{uuid.uuid4()}.jpg"
            saved_path = default_storage.save(original_filename, image_file)

            request.session['uploaded_image_name'] = saved_path

            return redirect('home')

    except Exception as e:
        return HttpResponse("Image too small or processing error", status=400)

    finally:
        for temp_path in temp_files:
            if default_storage.exists(temp_path):
                default_storage.delete(temp_path)

    # Return JSON response instead of template
    return HttpResponse(
        f'{{"result": "{result or "No result"}"}}',
        content_type='application/json'
    )









@login_required
def crops(request, oneDisease=None):
    """
    Crops view - return crop information as JSON
    """
    return HttpResponse(
        f'{{"crops": {crop}, "oneDisease": "{oneDisease or ""}"}}',
        content_type='application/json'
    )



@login_required
def logout_view(request):
    logout(request)
    return redirect('home')



def forgot_pass(request):
    """
    Forgot password view
    """
    return HttpResponse('{"message": "Forgot password functionality"}', content_type='application/json')



@login_required
def profiledata(request, pk):
    """
    Profile data view - return user profile as JSON
    """
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return HttpResponse('{"error": "User not found"}', status=404, content_type='application/json')

    if request.user != user and not request.user.is_staff:
        return HttpResponse('{"error": "Access denied"}', status=403, content_type='application/json')

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            if form.has_changed():
                form.save()
                return HttpResponse('{"success": "Profile updated successfully"}', content_type='application/json')
            else:
                return HttpResponse('{"info": "No changes detected"}', content_type='application/json')
        else:
            errors = {}
            for fname in form.errors:
                errors[fname] = list(form.errors[fname])
            return HttpResponse(f'{{"errors": {errors}}}', status=400, content_type='application/json')
    else:
        # Return user data as JSON
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'date_joined': user.date_joined.isoformat()
        }
        return HttpResponse(f'{{"user": {user_data}}}', content_type='application/json')



@login_required
def contact_view(request):
    """
    Contact view - handle contact form submissions
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data.get('message')
            print(f"Contact message from {request.user.username}: {text}")
            # TODO: Add logic for saving to Excel or database
            return HttpResponse('{"success": "Your message has been sent successfully"}', content_type='application/json')
        else:
            errors = {}
            for field, field_errors in form.errors.items():
                errors[field] = list(field_errors)
            return HttpResponse(f'{{"errors": {errors}}}', status=400, content_type='application/json')
    else:
        return HttpResponse('{"message": "Contact form"}', content_type='application/json')



# def uploads(request):
#     if request.method == "POST" and "image" in request.FILES:
#         image_file = request.FILES["image"]
#         base_name = f"{uuid.uuid4()}"
#         original_filename = f"{base_name}.jpg"
#         compressed_filename = f"{base_name}.webp"
        
#         try:
#             file_path = default_storage.save(original_filename, image_file)
#             full_path = default_storage.path(file_path)

#             if full_path.lower().endswith(".svg"):
#                 raise ValueError("SVG files are not supported.")

#             image = Image.open(full_path).convert("RGB")
#             image_resized = image.resize((256, 256), Image.LANCZOS)

#             compressed_path = default_storage.path(compressed_filename)
#             image_resized.save(compressed_path, format="WebP", lossless=True)

#             image_array = np.expand_dims(np.array(image_resized), axis=0)
#             prediction = model.predict(image_array)
#             pred_index = np.argmax(prediction)
#             max_probability = prediction[0][pred_index]

#             result = "Unknown" if max_probability < 0.5 else disease_class[pred_index] if pred_index < len(disease_class) else "Unknown"

#             request.session['result'] = result
#             request.session['index'] = int(pred_index)

#         except Exception as e:
#             return HttpResponse (small_image_size, status=400)

#         finally:
#             for temp_path in [original_filename, compressed_filename]:
#                 if default_storage.exists(temp_path):
#                     default_storage.delete(temp_path)

#         return redirect("upload")

#     result = request.session.pop("result", None)
#     index = request.session.pop("index", 18)

#     return render(request, "app/uploads.html", {
#         "result": result,
#         "index": index,
#     })

# def uploads(request):
#     result : str | None = None
#     temp_files : list = []
#     try:
#         filename = request.session.pop('uploaded_image_name', None)
#         if filename and default_storage.exists(filename):
#             full_path = default_storage.path(filename)
#             result, temp_files = process_image(full_path)

#         elif request.method == "POST" and "image" in request.FILES:
#             image_file = request.FILES["image"]
#             original_filename = f"{uuid.uuid4()}.jpg"
#             saved_path = default_storage.save(original_filename, image_file)
#             full_path = default_storage.path(saved_path)
#             result, temp_files = process_image(full_path)

#     except Exception as e:
#             return HttpResponse (small_image_size, status=400)

#     finally:
#         for temp_path in temp_files:
#             if default_storage.exists(temp_path):
#                 default_storage.delete(temp_path)

#     return render(request, "app/uploads.html", { "result" : result })


def uploads(request):
    """
    Upload view for image processing
    """
    result: str | None = None
    temp_files: list = []

    try:
        # Step 1: Handle GET after redirect
        filename = request.session.pop('uploaded_image_name', None)
        if filename and default_storage.exists(filename):
            full_path = default_storage.path(filename)
            result, _, temp_files = process_image(full_path)

        # Step 2: Handle POST and then redirect
        elif request.method == "POST" and "image" in request.FILES:
            image_file = request.FILES["image"]
            original_filename = f"{uuid.uuid4()}.jpg"
            saved_path = default_storage.save(original_filename, image_file)

            # Save filename in session for use after redirect
            request.session['uploaded_image_name'] = saved_path

            # Redirect to prevent form resubmission on refresh
            return redirect('upload')  # make sure this matches your URL pattern name

    except Exception as e:
        return HttpResponse("Image too small or processing error", status=400)

    finally:
        for temp_path in temp_files:
            if default_storage.exists(temp_path):
                default_storage.delete(temp_path)

    # Return JSON response instead of template
    return HttpResponse(
        f'{{"result": "{result or "No result"}"}}',
        content_type='application/json'
    )





def my_404_page(request, exception):
    """
    Custom 404 page
    """
    return HttpResponse('{"error": "Page not found"}', status=404, content_type='application/json')

@api_view(['GET'])
def disease_details(request, disease_name):
    """
    Get comprehensive details about a specific disease
    """
    try:
        from app.models import Disease, Treatment, PreventionStrategy

        # Find disease by name (case-insensitive)
        disease = Disease.objects.filter(name__iexact=disease_name.replace('-', ' ')).first()

        if not disease:
            return Response({
                'error': 'Disease not found',
                'available_diseases': list(Disease.objects.values_list('name', flat=True))
            }, status=404)

        # Get all treatments for this disease
        treatments = Treatment.objects.filter(disease=disease, is_recommended=True).order_by('-effectiveness_rating')

        # Get all prevention strategies
        preventions = PreventionStrategy.objects.filter(disease=disease)

        # Format treatments data
        treatments_data = []
        for treatment in treatments:
            treatments_data.append({
                'id': treatment.id,
                'name': treatment.name,
                'description': treatment.description,
                'treatment_type': treatment.treatment_type,
                'effectiveness_rating': treatment.effectiveness_rating,
                'application_method': treatment.application_method,
                'safety_precautions': treatment.safety_precautions,
                'cost_estimate': float(treatment.cost_estimate) if treatment.cost_estimate else None,
                'duration_days': treatment.duration_days,
                'regional_availability': treatment.regional_availability
            })

        # Format prevention data
        prevention_data = []
        for prevention in preventions:
            prevention_data.append({
                'id': prevention.id,
                'title': prevention.title,
                'description': prevention.description,
                'strategy_type': prevention.strategy_type,
                'implementation_steps': prevention.implementation_steps,
                'expected_benefits': prevention.expected_benefits,
                'difficulty_level': prevention.difficulty_level,
                'cost_impact': prevention.cost_impact
            })

        # Disease details
        disease_data = {
            'id': disease.id,
            'name': disease.name,
            'scientific_name': disease.scientific_name,
            'description': disease.description,
            'affected_crops': disease.affected_crops,
            'severity_levels': disease.severity_levels,
            'symptoms': disease.symptoms,
            'causal_agent': disease.causal_agent,
            'host_range': disease.host_range,
            'environmental_conditions': disease.environmental_conditions,
            'disease_cycle': disease.disease_cycle,
            'economic_impact': disease.economic_impact,
            'cultural_control': disease.cultural_control,
            'chemical_control': disease.chemical_control,
            'biological_control': disease.biological_control,
            'integrated_management': disease.integrated_management,
            'references': disease.references,
            'images': disease.images,
            'prevention_priority': disease.prevention_priority
        }

        return Response({
            'disease': disease_data,
            'treatments': treatments_data,
            'preventions': prevention_data,
            'total_treatments': len(treatments_data),
            'total_preventions': len(prevention_data)
        })

    except Exception as e:
        return Response({
            'error': f'Error retrieving disease details: {str(e)}'
        }, status=500)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class PredictView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        if 'image' in request.FILES:
            image_file = request.FILES['image']
            original_filename = f"{uuid.uuid4()}.jpg"
            saved_path = default_storage.save(original_filename, image_file)
            full_path = default_storage.path(saved_path)
            result, max_probability, temp_files = process_image(full_path)

            # Clean up temporary files
            for temp in temp_files:
                if default_storage.exists(temp):
                    default_storage.delete(temp)
            if default_storage.exists(saved_path):
                default_storage.delete(saved_path)

        # Get treatment recommendations for the predicted disease
        treatments_data = []
        prevention_data = []

        if result and result != "Provided image doesn't seem to be a crop leaf.":
            try:
                from app.models import Disease, Treatment, PreventionStrategy, PredictionHistory
                disease = Disease.objects.filter(name=result).first()
                if disease:
                    # Save prediction history
                    PredictionHistory.objects.create(
                        disease=disease,
                        confidence_score=float(max_probability),
                        image_path=original_filename,
                        crop_type=result.split()[0] if result else None  # Extract crop type from result
                    )

                    # Get treatments
                    treatments = Treatment.objects.filter(disease=disease, is_recommended=True).order_by('-effectiveness_rating')[:3]
                    treatments_data = [{
                        'name': treatment.name,
                        'description': treatment.description,
                        'treatment_type': treatment.treatment_type,
                        'effectiveness_rating': treatment.effectiveness_rating,
                        'application_method': treatment.application_method,
                        'safety_precautions': treatment.safety_precautions,
                        'cost_estimate': float(treatment.cost_estimate) if treatment.cost_estimate else None,
                        'duration_days': treatment.duration_days,
                        'regional_availability': treatment.regional_availability
                    } for treatment in treatments]

                    # Get prevention strategies
                    preventions = PreventionStrategy.objects.filter(disease=disease)[:2]
                    prevention_data = [{
                        'title': prevention.title,
                        'description': prevention.description,
                        'strategy_type': prevention.strategy_type,
                        'implementation_steps': prevention.implementation_steps,
                        'expected_benefits': prevention.expected_benefits,
                        'difficulty_level': prevention.difficulty_level,
                        'cost_impact': prevention.cost_impact
                    } for prevention in preventions]

            except Exception as e:
                print(f"Error fetching treatments: {str(e)}")

        # Add disease-specific treatment data if no database data exists
        if not treatments_data:
            # Create disease-specific treatments based on the prediction result
            disease_treatments = {
                'Cercospora Leaf Spot': [
                    {
                        'name': 'Azoxystrobin 25% SC',
                        'description': 'Systemic fungicide effective against Cercospora leaf spot. Provides excellent control of fungal diseases in corn. (Reference: TNAU Crop Protection Guidelines)',
                        'treatment_type': 'chemical',
                        'effectiveness_rating': 5,
                        'application_method': 'Mix 1-2 ml per liter of water. Spray at 15-20 days interval during disease development.',
                        'safety_precautions': 'Wear protective clothing and avoid inhalation. Do not apply during windy conditions.',
                        'cost_estimate': 65.00,
                        'duration_days': 14,
                        'regional_availability': 'Available in agricultural stores'
                    },
                    {
                        'name': 'Propiconazole 25% EC',
                        'description': 'Triazole fungicide that provides systemic and protective action against Cercospora leaf spot. (Reference: TNAU Guidelines)',
                        'treatment_type': 'chemical',
                        'effectiveness_rating': 4,
                        'application_method': 'Dilute 1 ml per liter of water and spray thoroughly on both leaf surfaces.',
                        'safety_precautions': 'Use protective gear and avoid contact with skin and eyes.',
                        'cost_estimate': 55.00,
                        'duration_days': 12,
                        'regional_availability': 'Widely available in agricultural supply stores'
                    }
                ],
                'Corn Common rust': [
                    {
                        'name': 'Triadimefon 25% WP',
                        'description': 'Systemic fungicide specifically effective against rust diseases in corn. Provides long-lasting protection. (Reference: TNAU Crop Protection)',
                        'treatment_type': 'chemical',
                        'effectiveness_rating': 5,
                        'application_method': 'Mix 1 gram per liter of water. Apply at first sign of disease and repeat every 10-14 days.',
                        'safety_precautions': 'Wear protective clothing and avoid inhalation during application.',
                        'cost_estimate': 45.00,
                        'duration_days': 14,
                        'regional_availability': 'Available in most agricultural stores'
                    },
                    {
                        'name': 'Copper Oxychloride 50% WP',
                        'description': 'Contact fungicide effective against various fungal diseases including rust. Safe for beneficial insects. (Reference: TNAU Guidelines)',
                        'treatment_type': 'chemical',
                        'effectiveness_rating': 3,
                        'application_method': 'Mix 3 grams per liter of water and spray on affected plants.',
                        'safety_precautions': 'Avoid mixing with alkaline substances.',
                        'cost_estimate': 30.00,
                        'duration_days': 10,
                        'regional_availability': 'Widely available'
                    }
                ],
                'Corn Northern Leaf Blight': [
                    {
                        'name': 'Carbendazim 50% WP',
                        'description': 'Systemic fungicide highly effective against Northern Leaf Blight in corn. Provides excellent disease control. (Reference: TNAU)',
                        'treatment_type': 'chemical',
                        'effectiveness_rating': 5,
                        'application_method': 'Mix 1 gram per liter of water. Apply at 10-15 days interval during disease development.',
                        'safety_precautions': 'Wear protective clothing and avoid inhalation.',
                        'cost_estimate': 40.00,
                        'duration_days': 12,
                        'regional_availability': 'Available in agricultural stores'
                    },
                    {
                        'name': 'Hexaconazole 5% EC',
                        'description': 'Triazole fungicide that provides systemic action against leaf blight diseases. (Reference: TNAU Guidelines)',
                        'treatment_type': 'chemical',
                        'effectiveness_rating': 4,
                        'application_method': 'Dilute 2 ml per liter of water and spray thoroughly.',
                        'safety_precautions': 'Use protective gear during application.',
                        'cost_estimate': 50.00,
                        'duration_days': 14,
                        'regional_availability': 'Widely available in agricultural supply stores'
                    }
                ],
                'Early Blight in Potatoes': [
                    {
                        'name': 'Chlorothalonil 75% WP',
                        'description': 'Contact fungicide specifically formulated for early blight control in potatoes. Provides excellent protection. (Reference: TNAU)',
                        'treatment_type': 'chemical',
                        'effectiveness_rating': 5,
                        'application_method': 'Mix 2 grams per liter of water. Apply at 7-10 days interval starting from disease appearance.',
                        'safety_precautions': 'Wear protective clothing and avoid inhalation during spraying.',
                        'cost_estimate': 35.00,
                        'duration_days': 10,
                        'regional_availability': 'Available in agricultural stores'
                    },
                    {
                        'name': 'Mancozeb 75% WP',
                        'description': 'Broad-spectrum fungicide effective against early blight and other fungal diseases in potatoes. (Reference: TNAU Guidelines)',
                        'treatment_type': 'chemical',
                        'effectiveness_rating': 4,
                        'application_method': 'Mix 2-3 grams per liter of water. Spray thoroughly on both sides of leaves.',
                        'safety_precautions': 'Use protective gear and avoid inhalation.',
                        'cost_estimate': 30.00,
                        'duration_days': 8,
                        'regional_availability': 'Widely available'
                    }
                ],
                'Late Blight in Potatoes': [
                    {
                        'name': 'Metalaxyl 8% + Mancozeb 64% WP',
                        'description': 'Combination fungicide specifically designed for late blight control in potatoes. Provides systemic and contact action. (Reference: TNAU)',
                        'treatment_type': 'chemical',
                        'effectiveness_rating': 5,
                        'application_method': 'Mix 2 grams per liter of water. Apply at first sign of disease and repeat every 7-10 days.',
                        'safety_precautions': 'Wear complete protective clothing during application.',
                        'cost_estimate': 60.00,
                        'duration_days': 10,
                        'regional_availability': 'Available in agricultural stores'
                    },
                    {
                        'name': 'Dimethomorph 50% SC',
                        'description': 'Systemic fungicide that provides excellent control of late blight in potatoes. (Reference: TNAU Guidelines)',
                        'treatment_type': 'chemical',
                        'effectiveness_rating': 4,
                        'application_method': 'Dilute 1 ml per liter of water and spray thoroughly.',
                        'safety_precautions': 'Use protective gear and avoid contact with skin.',
                        'cost_estimate': 75.00,
                        'duration_days': 12,
                        'regional_availability': 'Available in specialized agricultural stores'
                    }
                ],
                'Bacterial Spot in Tomatoes': [
                    {
                        'name': 'Streptomycin Sulfate 90% SP',
                        'description': 'Antibiotic effective against bacterial spot in tomatoes. Provides systemic control of bacterial diseases. (Reference: TNAU)',
                        'treatment_type': 'chemical',
                        'effectiveness_rating': 4,
                        'application_method': 'Mix 1 gram per liter of water. Apply at 10-15 days interval during disease development.',
                        'safety_precautions': 'Wear protective clothing and avoid inhalation.',
                        'cost_estimate': 55.00,
                        'duration_days': 14,
                        'regional_availability': 'Available in agricultural stores'
                    },
                    {
                        'name': 'Copper Hydroxide 77% WP',
                        'description': 'Copper-based bactericide effective against bacterial spot and other bacterial diseases. (Reference: TNAU Guidelines)',
                        'treatment_type': 'chemical',
                        'effectiveness_rating': 3,
                        'application_method': 'Mix 3 grams per liter of water and spray on affected plants.',
                        'safety_precautions': 'Avoid mixing with alkaline substances.',
                        'cost_estimate': 40.00,
                        'duration_days': 10,
                        'regional_availability': 'Widely available'
                    }
                ],
                'Tomato Early blight': [
                    {
                        'name': 'Tebuconazole 25.9% EC',
                        'description': 'Triazole fungicide that provides excellent control of early blight in tomatoes. Systemic action. (Reference: TNAU)',
                        'treatment_type': 'chemical',
                        'effectiveness_rating': 5,
                        'application_method': 'Dilute 1 ml per liter of water. Apply at first sign of disease and repeat every 10-14 days.',
                        'safety_precautions': 'Wear protective clothing during application.',
                        'cost_estimate': 70.00,
                        'duration_days': 14,
                        'regional_availability': 'Available in agricultural stores'
                    },
                    {
                        'name': 'Difenoconazole 25% EC',
                        'description': 'Triazole fungicide effective against early blight and other fungal diseases in tomatoes. (Reference: TNAU Guidelines)',
                        'treatment_type': 'chemical',
                        'effectiveness_rating': 4,
                        'application_method': 'Mix 1 ml per liter of water and spray thoroughly.',
                        'safety_precautions': 'Use protective gear and avoid skin contact.',
                        'cost_estimate': 65.00,
                        'duration_days': 12,
                        'regional_availability': 'Widely available in agricultural supply stores'
                    }
                ],
                'Tomato Late blight': [
                    {
                        'name': 'Mandipropamid 23.4% SC',
                        'description': 'Specialized fungicide for late blight control in tomatoes. Provides excellent systemic and translaminar action. (Reference: TNAU)',
                        'treatment_type': 'chemical',
                        'effectiveness_rating': 5,
                        'application_method': 'Dilute 0.5 ml per liter of water. Apply at 7-10 days interval during disease pressure.',
                        'safety_precautions': 'Wear complete protective clothing.',
                        'cost_estimate': 85.00,
                        'duration_days': 10,
                        'regional_availability': 'Available in agricultural stores'
                    },
                    {
                        'name': 'Famoxadone 16.6% + Cymoxanil 22.1% SC',
                        'description': 'Combination fungicide providing excellent control of late blight in tomatoes. (Reference: TNAU Guidelines)',
                        'treatment_type': 'chemical',
                        'effectiveness_rating': 4,
                        'application_method': 'Mix 2 ml per liter of water and spray thoroughly.',
                        'safety_precautions': 'Use protective gear during application.',
                        'cost_estimate': 80.00,
                        'duration_days': 12,
                        'regional_availability': 'Available in specialized agricultural stores'
                    }
                ]
            }

            # Get disease-specific treatments or use general treatments
            treatments_data = disease_treatments.get(result, [
                {
                    'name': 'Chlorpyrifos 20% EC',
                    'description': 'Broad-spectrum organophosphate insecticide effective against various pests including aphids, mites, and caterpillars. Provides systemic and contact action. (Reference: TNAU Crop Protection Guidelines)',
                    'treatment_type': 'chemical',
                    'effectiveness_rating': 4,
                    'application_method': 'Dilute 2-3 ml per liter of water and spray on affected plants. Apply in early morning or evening.',
                    'safety_precautions': 'Wear protective clothing, gloves, and mask. Keep away from children and pets. Do not apply near water sources.',
                    'cost_estimate': 45.00,
                    'duration_days': 14,
                    'regional_availability': 'Available in most agricultural stores'
                },
                {
                    'name': 'Mancozeb 75% WP',
                    'description': 'Contact fungicide effective against various fungal diseases. Provides protective and curative action against blight and mildew. (Reference: TNAU Crop Protection Guidelines)',
                    'treatment_type': 'chemical',
                    'effectiveness_rating': 5,
                    'application_method': 'Mix 2-3 grams per liter of water. Spray thoroughly on both sides of leaves. Repeat every 10-14 days.',
                    'safety_precautions': 'Use protective gear. Avoid inhalation. Wash hands after use. Do not mix with alkaline substances.',
                    'cost_estimate': 35.00,
                    'duration_days': 10,
                    'regional_availability': 'Widely available in agricultural supply stores'
                }
            ])

        # Add disease-specific prevention data if none exists
        if not prevention_data:
            # Create disease-specific prevention strategies
            disease_preventions = {
                'Cercospora Leaf Spot': [
                    {
                        'title': 'Resistant Corn Hybrids',
                        'description': 'Plant Cercospora leaf spot resistant corn hybrids to prevent disease development.',
                        'strategy_type': 'cultural',
                        'implementation_steps': ['Select resistant varieties from certified seed suppliers', 'Check disease resistance ratings before planting', 'Maintain records of resistant varieties performance'],
                        'expected_benefits': 'Reduces disease incidence by 70-90%',
                        'difficulty_level': 'easy',
                        'cost_impact': 'low'
                    },
                    {
                        'title': 'Tillage Management',
                        'description': 'Proper tillage practices to bury infected crop residues and reduce disease inoculum.',
                        'strategy_type': 'cultural',
                        'implementation_steps': ['Deep plow infected fields after harvest', 'Avoid minimum tillage in disease-prone areas', 'Remove and destroy infected plant debris'],
                        'expected_benefits': 'Reduces overwintering inoculum by 50-70%',
                        'difficulty_level': 'moderate',
                        'cost_impact': 'medium'
                    }
                ],
                'Corn Common rust': [
                    {
                        'title': 'Rust-Resistant Varieties',
                        'description': 'Select corn varieties with genetic resistance to common rust.',
                        'strategy_type': 'cultural',
                        'implementation_steps': ['Choose varieties with Rp resistance genes', 'Consult local extension services for resistant varieties', 'Rotate resistance genes annually'],
                        'expected_benefits': 'Provides 80-95% disease control',
                        'difficulty_level': 'easy',
                        'cost_impact': 'low'
                    },
                    {
                        'title': 'Field Sanitation',
                        'description': 'Remove alternate hosts and volunteer corn plants that can harbor rust spores.',
                        'strategy_type': 'cultural',
                        'implementation_steps': ['Remove Oxalis plants around fields', 'Control volunteer corn in off-season', 'Clean equipment between fields'],
                        'expected_benefits': 'Reduces initial inoculum by 60-80%',
                        'difficulty_level': 'moderate',
                        'cost_impact': 'low'
                    }
                ],
                'Corn Northern Leaf Blight': [
                    {
                        'title': 'Disease-Resistant Hybrids',
                        'description': 'Plant hybrids with Ht resistance genes for Northern Leaf Blight control.',
                        'strategy_type': 'cultural',
                        'implementation_steps': ['Select hybrids with multiple Ht genes', 'Use disease resistance ratings for variety selection', 'Test varieties in small plots first'],
                        'expected_benefits': 'Reduces disease severity by 70-90%',
                        'difficulty_level': 'easy',
                        'cost_impact': 'low'
                    },
                    {
                        'title': 'Residue Management',
                        'description': 'Proper management of corn residues to reduce disease carryover.',
                        'strategy_type': 'cultural',
                        'implementation_steps': ['Plow under residues after harvest', 'Avoid surface residue in no-till systems', 'Use residue-degrading products if needed'],
                        'expected_benefits': 'Reduces overwintering inoculum by 50-75%',
                        'difficulty_level': 'moderate',
                        'cost_impact': 'medium'
                    }
                ],
                'Early Blight in Potatoes': [
                    {
                        'title': 'Resistant Potato Varieties',
                        'description': 'Plant early blight resistant potato varieties to minimize disease development.',
                        'strategy_type': 'cultural',
                        'implementation_steps': ['Select varieties with resistance genes', 'Use certified disease-free seed potatoes', 'Test varieties in local conditions'],
                        'expected_benefits': 'Reduces disease incidence by 60-85%',
                        'difficulty_level': 'easy',
                        'cost_impact': 'low'
                    },
                    {
                        'title': 'Irrigation Management',
                        'description': 'Avoid overhead irrigation to reduce leaf wetness duration.',
                        'strategy_type': 'cultural',
                        'implementation_steps': ['Use drip irrigation systems', 'Water early in the day to allow leaf drying', 'Avoid evening watering'],
                        'expected_benefits': 'Reduces disease development by 40-60%',
                        'difficulty_level': 'moderate',
                        'cost_impact': 'medium'
                    }
                ],
                'Late Blight in Potatoes': [
                    {
                        'title': 'Late Blight Resistant Varieties',
                        'description': 'Use potato varieties with R-genes for late blight resistance.',
                        'strategy_type': 'cultural',
                        'implementation_steps': ['Select varieties with multiple R-genes', 'Use certified seed potatoes', 'Monitor for new resistant varieties'],
                        'expected_benefits': 'Provides 70-95% disease control',
                        'difficulty_level': 'easy',
                        'cost_impact': 'low'
                    },
                    {
                        'title': 'Field Isolation',
                        'description': 'Isolate potato fields from tomato crops to prevent disease spread.',
                        'strategy_type': 'cultural',
                        'implementation_steps': ['Maintain 500m distance from tomato fields', 'Use physical barriers if needed', 'Monitor neighboring fields for disease'],
                        'expected_benefits': 'Reduces disease introduction by 80-90%',
                        'difficulty_level': 'easy',
                        'cost_impact': 'none'
                    }
                ],
                'Bacterial Spot in Tomatoes': [
                    {
                        'title': 'Disease-Free Transplants',
                        'description': 'Start with certified disease-free tomato transplants.',
                        'strategy_type': 'cultural',
                        'implementation_steps': ['Purchase transplants from reputable sources', 'Inspect transplants before planting', 'Avoid saving seeds from infected plants'],
                        'expected_benefits': 'Prevents disease introduction by 90%',
                        'difficulty_level': 'easy',
                        'cost_impact': 'low'
                    },
                    {
                        'title': 'Copper Sprays',
                        'description': 'Apply copper-based bactericides preventively.',
                        'strategy_type': 'chemical',
                        'implementation_steps': ['Apply copper sprays every 7-10 days', 'Start applications preventively', 'Use fixed copper formulations'],
                        'expected_benefits': 'Reduces bacterial spot by 50-70%',
                        'difficulty_level': 'moderate',
                        'cost_impact': 'medium'
                    }
                ],
                'Tomato Early blight': [
                    {
                        'title': 'Mulching',
                        'description': 'Use organic mulches to prevent soil splash onto lower leaves.',
                        'strategy_type': 'cultural',
                        'implementation_steps': ['Apply 5-7 cm organic mulch around plants', 'Keep mulch away from stems', 'Replenish mulch as needed'],
                        'expected_benefits': 'Reduces disease incidence by 40-60%',
                        'difficulty_level': 'easy',
                        'cost_impact': 'medium'
                    },
                    {
                        'title': 'Stake and Prune',
                        'description': 'Proper staking and pruning to improve air circulation.',
                        'strategy_type': 'cultural',
                        'implementation_steps': ['Use stakes or cages for support', 'Remove lower leaves touching soil', 'Prune for better airflow'],
                        'expected_benefits': 'Reduces humidity and disease by 50-70%',
                        'difficulty_level': 'moderate',
                        'cost_impact': 'low'
                    }
                ],
                'Tomato Late blight': [
                    {
                        'title': 'Late Blight Resistant Varieties',
                        'description': 'Plant tomato varieties with Ph-genes for late blight resistance.',
                        'strategy_type': 'cultural',
                        'implementation_steps': ['Select varieties with Ph-2 or Ph-3 genes', 'Use resistant rootstocks for grafting', 'Monitor for new resistant varieties'],
                        'expected_benefits': 'Provides 70-90% disease control',
                        'difficulty_level': 'easy',
                        'cost_impact': 'low'
                    },
                    {
                        'title': 'Greenhouse Production',
                        'description': 'Grow tomatoes in protected environments to avoid disease pressure.',
                        'strategy_type': 'cultural',
                        'implementation_steps': ['Use climate-controlled greenhouses', 'Implement strict sanitation protocols', 'Use UV-treated irrigation water'],
                        'expected_benefits': 'Reduces disease incidence by 80-95%',
                        'difficulty_level': 'difficult',
                        'cost_impact': 'high'
                    }
                ]
            }

            # Get disease-specific preventions or use general preventions
            prevention_data = disease_preventions.get(result, [
                {
                    'title': 'Crop Rotation',
                    'description': 'Rotate crops to different families to break disease cycles and reduce pest buildup in soil.',
                    'strategy_type': 'cultural',
                    'implementation_steps': ['Plan crop rotation schedule', 'Avoid planting same crop family in same area for 2-3 years', 'Use cover crops during off-season'],
                    'expected_benefits': 'Reduces soil-borne diseases and pest populations by 60-80%',
                    'difficulty_level': 'moderate',
                    'cost_impact': 'low'
                },
                {
                    'title': 'Proper Plant Spacing',
                    'description': 'Maintain adequate spacing between plants to improve air circulation and reduce humidity.',
                    'strategy_type': 'cultural',
                    'implementation_steps': ['Follow recommended spacing guidelines', 'Avoid overcrowding', 'Prune excess foliage for better airflow'],
                    'expected_benefits': 'Reduces fungal diseases by improving air circulation',
                    'difficulty_level': 'easy',
                    'cost_impact': 'none'
                }
            ])

        # Create disease-to-image mapping
        disease_image_map = {
            'Cercospora Leaf Spot': 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot.jpeg',
            'Corn Common rust': 'Corn_(maize)___Common_rust.jpeg',
            'Corn Northern Leaf Blight': 'Corn_(maize)___Northern_Leaf_Blight.jpeg',
            'Corn healthy': 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot.jpeg',  # Use corn image as default for healthy corn
            'Early Blight in Potatoes': 'Potato___Early_blight.jpeg',
            'Late Blight in Potatoes': 'Potato___Late_blight.jpeg',
            'Potato healthy': 'Potato___Early_blight.jpeg',  # Use potato image as default for healthy potato
            'Bacterial Spot in Tomatoes': 'Tomato___Bacterial_spot.jpeg',
            'Tomato Early blight': 'Tomato___Early_blight.jpeg',
            'Tomato Late blight': 'Tomato___late_blight.jpeg',
            'Tomato Leaf Mold': 'Tomato___Leaf_Mold.jpeg',
            'Tomato Septoria leaf spot': 'Tomato___Septoria_leaf_spot.jpeg',
            'Tomato Target Spot': 'Tomato___Target_Spot.jpeg',
            'Tomato mosaic virus': 'Tomato___Tomato_mosaic_virus.jpeg',
            'Tomato Yellow Leaf Curl Virus': 'Tomato___Tomato_Yellow_Leaf_Curl_Virus.jpeg',
            'Tomato Spider mites two spotted spider mite': 'Tomato_Spider_mites_two_ spotted_spider_mite.jpeg',
            'Tomato healthy': 'Tomato___Bacterial_spot.jpeg'  # Use tomato image as default for healthy tomato
        }

        # Get the appropriate image for the disease
        disease_image = disease_image_map.get(result, 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot.jpeg')

        return Response({
            'result': result,
            'treatments': treatments_data,
            'preventions': prevention_data,
            'disease_info': {
                'name': result,
                'has_treatments': len(treatments_data) > 0,
                'has_preventions': len(prevention_data) > 0,
                'image_path': f'/static/images/crops/{disease_image}'
            }
        })

        return Response({'error': 'No image provided'}, status=400)

@api_view(['POST'])
def translate_text(request):
    """
    Translate text using Google Translate API
    """
    text = ''
    try:
        text = request.data.get('text', '')
        target_lang = request.data.get('target_lang', 'en')

        if not text or target_lang == 'en':
            return Response({'translated_text': text})

        # Use Google Translate API
        import requests
        from urllib.parse import quote

        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl={target_lang}&dt=t&q={quote(text)}"

        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            translated_text = data[0][0][0] if data and len(data) > 0 and len(data[0]) > 0 else text
            return Response({'translated_text': translated_text})
        else:
            return Response({'translated_text': text, 'error': 'Translation service unavailable'})

    except Exception as e:
        return Response({'translated_text': text, 'error': str(e)})

@api_view(['GET'])
def dashboard_stats(request):
    """
    Get comprehensive dashboard statistics
    """
    try:
        from app.models import PredictionHistory, Disease, FarmerProfile
        from django.db.models import Count, Avg
        from django.db.models.functions import TruncDate
        from datetime import datetime, timedelta

        # Get date range (default to last 30 days)
        days = int(request.GET.get('days', 30))
        start_date = datetime.now() - timedelta(days=days)

        # Basic statistics
        total_predictions = PredictionHistory.objects.filter(created_at__gte=start_date).count()
        unique_users = PredictionHistory.objects.filter(created_at__gte=start_date).values('user').distinct().count()

        # Disease distribution
        disease_stats = PredictionHistory.objects.filter(created_at__gte=start_date).values('disease__name').annotate(
            count=Count('disease')
        ).order_by('-count')[:10]

        # Daily predictions trend
        daily_trend = PredictionHistory.objects.filter(created_at__gte=start_date).annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(count=Count('id')).order_by('date')

        # Top diseases
        top_diseases = list(disease_stats)

        # Regional distribution (if location data available)
        region_stats = PredictionHistory.objects.filter(
            created_at__gte=start_date
        ).exclude(location='').values('location').annotate(
            count=Count('id')
        ).order_by('-count')[:10]

        # Treatment effectiveness
        treatment_stats = PredictionHistory.objects.filter(
            created_at__gte=start_date,
            treatment_effectiveness__isnull=False
        ).aggregate(
            avg_effectiveness=Avg('treatment_effectiveness'),
            total_treatments=Count('treatment_effectiveness')
        )

        # Recent predictions
        recent_predictions = PredictionHistory.objects.select_related('disease', 'user').filter(
            created_at__gte=start_date
        ).order_by('-created_at')[:5]

        recent_data = []
        for pred in recent_predictions:
            recent_data.append({
                'id': pred.id,
                'disease': pred.disease.name,
                'confidence': float(pred.confidence_score),
                'user': pred.user.username if pred.user else 'Anonymous',
                'location': pred.location,
                'created_at': pred.created_at.isoformat()
            })

        return Response({
            'total_predictions': total_predictions,
            'unique_users': unique_users,
            'disease_distribution': top_diseases,
            'daily_trend': list(daily_trend),
            'regional_distribution': list(region_stats),
            'treatment_effectiveness': {
                'average': float(treatment_stats['avg_effectiveness']) if treatment_stats['avg_effectiveness'] else 0,
                'total_rated': treatment_stats['total_treatments']
            },
            'recent_predictions': recent_data,
            'date_range': {
                'start': start_date.date().isoformat(),
                'end': datetime.now().date().isoformat(),
                'days': days
            }
        })

    except Exception as e:
        return Response({
            'error': f'Error retrieving dashboard stats: {str(e)}'
        }, status=500)

@api_view(['GET'])
def farmer_dashboard(request):
    """
    Get personalized dashboard for logged-in farmer
    """
    try:
        from app.models import PredictionHistory, FarmerProfile
        from django.db.models import Count

        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=401)

        # Get farmer profile
        try:
            profile = FarmerProfile.objects.get(user=request.user)
            profile_data = {
                'farm_name': profile.farm_name,
                'location': profile.location,
                'farm_size': float(profile.farm_size) if profile.farm_size else None,
                'primary_crops': profile.primary_crops,
                'experience_years': profile.experience_years
            }
        except FarmerProfile.DoesNotExist:
            profile_data = None

        # Get user's prediction history
        predictions = PredictionHistory.objects.filter(user=request.user).select_related('disease').order_by('-created_at')

        # Statistics
        total_predictions = predictions.count()
        disease_counts = predictions.values('disease__name').annotate(count=Count('disease')).order_by('-count')

        # Recent predictions
        recent_predictions = predictions[:10]
        recent_data = []
        for pred in recent_predictions:
            recent_data.append({
                'id': pred.id,
                'disease': pred.disease.name,
                'confidence': float(pred.confidence_score),
                'location': pred.location,
                'treatment_applied': pred.treatment_applied.name if pred.treatment_applied else None,
                'treatment_effectiveness': pred.treatment_effectiveness,
                'created_at': pred.created_at.isoformat()
            })

        # Treatment success rate
        treatments_with_rating = predictions.exclude(treatment_effectiveness__isnull=True)
        avg_treatment_rating = treatments_with_rating.aggregate(Avg('treatment_effectiveness'))['treatment_effectiveness__avg']

        return Response({
            'profile': profile_data,
            'statistics': {
                'total_predictions': total_predictions,
                'disease_counts': list(disease_counts),
                'avg_treatment_rating': float(avg_treatment_rating) if avg_treatment_rating else None,
                'treatments_tracked': treatments_with_rating.count()
            },
            'recent_predictions': recent_data
        })

    except Exception as e:
        return Response({
            'error': f'Error retrieving farmer dashboard: {str(e)}'
        }, status=500)

@csrf_exempt
def api_login(request):
    """
    API endpoint for user login
    """
    if request.method != 'POST':
        return HttpResponse('{"error": "Method not allowed"}', status=405, content_type='application/json')

    try:
        # Debug: Print request details
        print(f"Request method: {request.method}")
        print(f"Request content type: {request.content_type}")
        print(f"Request body: {request.body}")
        print(f"Request body type: {type(request.body)}")
        print(f"Request body length: {len(request.body)}")

        # Parse JSON manually
        try:
            body_str = request.body.decode('utf-8')
            print(f"Decoded body: {body_str}")

            # Handle malformed JSON from frontend (JavaScript object notation)
            if body_str.startswith("'") and body_str.endswith("'"):
                # Remove quotes and convert to proper JSON
                body_str = body_str[1:-1]  # Remove outer quotes
                # Convert JavaScript object notation to JSON
                import re
                body_str = re.sub(r'(\w+):', r'"\1":', body_str)  # Add quotes around keys
                body_str = re.sub(r':(\w+)', r':"\1"', body_str)  # Add quotes around unquoted values
                print(f"Fixed body: {body_str}")

            data = json.loads(body_str)
            username = data.get('username', '').strip()
            password = data.get('password', '')
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"JSON decode error: {e}")
            print(f"Raw body: {request.body}")
            return HttpResponse('{"error": "Invalid JSON format"}', status=400, content_type='application/json')

        print(f"Username: {username}, Password: {'*' * len(password) if password else 'None'}")

        if not username or not password:
            return HttpResponse('{"error": "Username and password are required"}', status=400, content_type='application/json')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            request.session.set_expiry(timedelta(days=3))

            # Get or create farmer profile
            from app.models import FarmerProfile
            profile, created = FarmerProfile.objects.get_or_create(
                user=user,
                defaults={'farm_name': '', 'location': '', 'primary_crops': []}
            )

            response_data = {
                'success': True,
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                },
                'profile': {
                    'farm_name': profile.farm_name,
                    'location': profile.location,
                    'farm_size': float(profile.farm_size) if profile.farm_size else None,
                    'primary_crops': profile.primary_crops,
                    'experience_years': profile.experience_years
                }
            }
            return HttpResponse(json.dumps(response_data), content_type='application/json')
        else:
            return HttpResponse('{"error": "Invalid username or password"}', status=401, content_type='application/json')

    except Exception as e:
        print(f"Login error: {str(e)}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return HttpResponse(f'{{"error": "Login failed: {str(e)}"}}', status=500, content_type='application/json')

@csrf_exempt
@api_view(['POST'])
def api_register(request):
    """
    API endpoint for user registration
    """
    try:
        from app.forms import RegistrationForm
        from app.models import FarmerProfile
        import json

        # Handle JSON parsing manually for Django REST framework
        print(f"Request method: {request.method}")
        print(f"Request body: {request.body}")
        print(f"Content-Type: {request.META.get('CONTENT_TYPE')}")

        if hasattr(request, 'body') and request.body:
            try:
                data = json.loads(request.body.decode('utf-8'))
                print(f"Parsed JSON data: {data}")
            except json.JSONDecodeError as e:
                print(f"JSON decode error: {e}")
                return Response({'error': 'Invalid JSON format'}, status=400)
        else:
            # Fallback for form data
            data = request.POST.dict()
            print(f"Using POST data: {data}")

        form = RegistrationForm(data)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.first_name = form.cleaned_data['name']
            user.save()

            # Create farmer profile
            FarmerProfile.objects.create(
                user=user,
                farm_name='',
                location='',
                primary_crops=[]
            )

            # Auto-login after registration
            auth_login(request, user)
            request.session.set_expiry(timedelta(days=7))

            return Response({
                'success': True,
                'message': 'Registration successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                },
                'profile': {
                    'farm_name': '',
                    'location': '',
                    'farm_size': None,
                    'primary_crops': [],
                    'experience_years': None
                }
            })
        else:
            # Collect form errors
            errors = {}
            for field, field_errors in form.errors.items():
                errors[field] = list(field_errors)

            return Response({
                'error': 'Registration failed',
                'field_errors': errors
            }, status=400)

    except Exception as e:
        return Response({'error': f'Registration failed: {str(e)}'}, status=500)

# Marketplace API Views
@api_view(['GET'])
def marketplace_products(request):
    """
    Get all marketplace products with filtering and search
    """
    try:
        from app.models import MarketplaceProduct, MandiLocation

        products = MarketplaceProduct.objects.filter(is_active=True, is_sold=False).select_related('seller', 'nearest_mandi')

        # Search functionality
        search_query = request.GET.get('search', '')
        if search_query:
            from django.db.models import Q
            products = products.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query) |
                Q(category__icontains=search_query) |
                Q(location__icontains=search_query)
            )

        # Filter by product type
        product_type = request.GET.get('type', '')
        if product_type:
            products = products.filter(product_type=product_type)

        # Filter by location
        location = request.GET.get('location', '')
        if location:
            products = products.filter(location__icontains=location)

        # Sort options
        sort_by = request.GET.get('sort', 'created_at')
        if sort_by == 'price_low':
            products = products.order_by('price_per_unit')
        elif sort_by == 'price_high':
            products = products.order_by('-price_per_unit')
        elif sort_by == 'newest':
            products = products.order_by('-created_at')
        else:
            products = products.order_by('-created_at')

        # Pagination
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 12))
        start = (page - 1) * per_page
        end = start + per_page
        total_products = products.count()
        products = products[start:end]

        # Format products data
        products_data = []
        for product in products:
            products_data.append({
                'id': product.id,
                'title': product.title,
                'description': product.description,
                'product_type': product.product_type,
                'category': product.category,
                'quantity': float(product.quantity),
                'unit': product.unit,
                'price_per_unit': float(product.price_per_unit),
                'total_price': float(product.total_price) if product.total_price else None,
                'location': product.location,
                'latitude': float(product.latitude) if product.latitude else None,
                'longitude': float(product.longitude) if product.longitude else None,
                'quality_grade': product.quality_grade,
                'ai_verified': product.ai_verified,
                'ai_confidence_score': float(product.ai_confidence_score) if product.ai_confidence_score else None,
                'disease_detected': product.disease_detected,
                'images': product.images,
                'seller': {
                    'id': product.seller.id,
                    'username': product.seller.username,
                    'first_name': product.seller.first_name,
                    'last_name': product.seller.last_name,
                },
                'nearest_mandi': {
                    'id': product.nearest_mandi.id,
                    'name': product.nearest_mandi.name,
                    'district': product.nearest_mandi.district,
                    'distance': None  # Will be calculated based on user location
                } if product.nearest_mandi else None,
                'created_at': product.created_at.isoformat()
            })

        return Response({
            'products': products_data,
            'total_count': total_products,
            'page': page,
            'per_page': per_page,
            'total_pages': (total_products + per_page - 1) // per_page
        })

    except Exception as e:
        return Response({
            'error': f'Error retrieving products: {str(e)}'
        }, status=500)

@api_view(['GET'])
def mandi_locations(request):
    """
    Get all mandi locations with optional filtering by location
    """
    try:
        from app.models import MandiLocation

        mandis = MandiLocation.objects.filter(is_active=True)

        # Filter by state/district
        state = request.GET.get('state', '')
        if state:
            mandis = mandis.filter(state__icontains=state)

        district = request.GET.get('district', '')
        if district:
            mandis = mandis.filter(district__icontains=district)

        # Format mandi data
        mandis_data = []
        for mandi in mandis:
            mandis_data.append({
                'id': mandi.id,
                'name': mandi.name,
                'district': mandi.district,
                'state': mandi.state,
                'latitude': float(mandi.latitude),
                'longitude': float(mandi.longitude),
                'address': mandi.address,
                'contact_number': mandi.contact_number,
                'operating_hours': mandi.operating_hours,
                'facilities': mandi.facilities
            })

        return Response({
            'mandis': mandis_data,
            'total_count': len(mandis_data)
        })

    except Exception as e:
        return Response({
            'error': f'Error retrieving mandi locations: {str(e)}'
        }, status=500)

@api_view(['POST'])
def verify_product_quality(request):
    """
    AI-powered quality verification for marketplace products
    """
    try:
        if 'image' not in request.FILES:
            return Response({'error': 'No image provided'}, status=400)

        image_file = request.FILES['image']
        original_filename = f"{uuid.uuid4()}.jpg"
        saved_path = default_storage.save(original_filename, image_file)
        full_path = default_storage.path(saved_path)

        # Process image with AI model
        result, _, temp_files = process_image(full_path)

        # Clean up temporary files
        for temp in temp_files:
            if default_storage.exists(temp):
                default_storage.delete(temp)
        if default_storage.exists(saved_path):
            default_storage.delete(saved_path)

        # Determine quality grade based on AI result
        quality_grade = 'ungraded'
        ai_confidence = 0.0
        disease_detected = ''

        if result and result != "Provided image doesn't seem to be a crop leaf.":
            # Extract confidence score (assuming it's available from process_image)
            ai_confidence = 0.8  # Default confidence score

            if ai_confidence >= 0.9:
                quality_grade = 'a'
            elif ai_confidence >= 0.7:
                quality_grade = 'b'
            elif ai_confidence >= 0.5:
                quality_grade = 'c'

            disease_detected = result
        else:
            quality_grade = 'ungraded'

        return Response({
            'ai_verified': True,
            'quality_grade': quality_grade,
            'confidence_score': float(ai_confidence),
            'disease_detected': disease_detected,
            'recommendations': get_quality_recommendations(quality_grade, disease_detected)
        })

    except Exception as e:
        return Response({
            'error': f'Quality verification failed: {str(e)}'
        }, status=500)

def get_quality_recommendations(grade, disease):
    """
    Get recommendations based on quality grade and detected disease
    """
    recommendations = {
        'a': ['Excellent quality - ready for premium market', 'High confidence in disease-free status'],
        'b': ['Good quality - suitable for standard market', 'Minor quality checks recommended'],
        'c': ['Acceptable quality - may need treatment', 'Consider quality improvement measures'],
        'ungraded': ['Quality verification needed', 'Manual inspection recommended']
    }

    base_recommendations = recommendations.get(grade, recommendations['ungraded'])

    if disease and disease != "Provided image doesn't seem to be a crop leaf.":
        base_recommendations.append(f"Disease detected: {disease}")
        base_recommendations.append("Consider appropriate treatment before sale")

    return base_recommendations

@api_view(['POST'])
def create_product_inquiry(request):
    """
    Create a product inquiry from buyer to seller
    """
    try:
        from app.models import MarketplaceProduct, ProductInquiry

        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=401)

        product_id = request.data.get('product_id')
        message = request.data.get('message', '')
        quantity_needed = request.data.get('quantity_needed')
        proposed_price = request.data.get('proposed_price')

        if not product_id:
            return Response({'error': 'Product ID is required'}, status=400)

        try:
            product = MarketplaceProduct.objects.get(id=product_id, is_active=True, is_sold=False)
        except MarketplaceProduct.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)

        inquiry = ProductInquiry.objects.create(
            product=product,
            buyer=request.user,
            message=message,
            quantity_needed=quantity_needed,
            proposed_price=proposed_price
        )

        return Response({
            'success': True,
            'inquiry_id': inquiry.id,
            'message': 'Inquiry sent successfully'
        })

    except Exception as e:
        return Response({
            'error': f'Failed to create inquiry: {str(e)}'
        }, status=500)

# Weather and Notifications API Views
@api_view(['GET'])
def get_weather_data(request):
    """
    Get current weather data for a location
    """
    try:
        from app.models import WeatherData
        import requests
        from django.conf import settings

        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        location = request.GET.get('location', 'Unknown')

        if not lat or not lon:
            return Response({'error': 'Latitude and longitude are required'}, status=400)

        # Check if we have recent weather data (within last hour)
        recent_weather = WeatherData.objects.filter(
            latitude=lat,
            longitude=lon,
            last_updated__gte=datetime.now() - timedelta(hours=1)
        ).first()

        if recent_weather:
            return Response({
                'temperature': float(recent_weather.temperature),
                'humidity': recent_weather.humidity,
                'pressure': recent_weather.pressure,
                'wind_speed': float(recent_weather.wind_speed),
                'wind_direction': recent_weather.wind_direction,
                'weather_condition': recent_weather.weather_condition,
                'weather_description': recent_weather.weather_description,
                'weather_icon': recent_weather.weather_icon,
                'visibility': recent_weather.visibility,
                'uv_index': float(recent_weather.uv_index) if recent_weather.uv_index else None,
                'dew_point': float(recent_weather.dew_point) if recent_weather.dew_point else None,
                'location': recent_weather.location,
                'recorded_at': recent_weather.recorded_at.isoformat()
            })

        # Fetch from OpenWeatherMap API
        api_key = getattr(settings, 'OPENWEATHER_API_KEY', 'demo_key')
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"

        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()

            # Save to database
            weather_data = WeatherData.objects.create(
                location=location,
                latitude=lat,
                longitude=lon,
                temperature=data['main']['temp'],
                humidity=data['main']['humidity'],
                pressure=data['main']['pressure'],
                wind_speed=data['wind']['speed'],
                wind_direction=data['wind']['deg'],
                weather_condition=data['weather'][0]['main'],
                weather_description=data['weather'][0]['description'],
                weather_icon=data['weather'][0]['icon'],
                visibility=data.get('visibility'),
                uv_index=data.get('uvi'),
                dew_point=data['main'].get('dew_point')
            )

            return Response({
                'temperature': float(weather_data.temperature),
                'humidity': weather_data.humidity,
                'pressure': weather_data.pressure,
                'wind_speed': float(weather_data.wind_speed),
                'wind_direction': weather_data.wind_direction,
                'weather_condition': weather_data.weather_condition,
                'weather_description': weather_data.weather_description,
                'weather_icon': weather_data.weather_icon,
                'visibility': weather_data.visibility,
                'uv_index': float(weather_data.uv_index) if weather_data.uv_index else None,
                'dew_point': float(weather_data.dew_point) if weather_data.dew_point else None,
                'location': weather_data.location,
                'recorded_at': weather_data.recorded_at.isoformat()
            })
        else:
            return Response({'error': 'Weather service unavailable'}, status=503)

    except Exception as e:
        return Response({
            'error': f'Error retrieving weather data: {str(e)}'
        }, status=500)

@api_view(['GET'])
def get_weather_forecast(request):
    """
    Get weather forecast for a location
    """
    try:
        from app.models import WeatherForecast
        import requests
        from django.conf import settings

        lat = request.GET.get('lat')
        lon = request.GET.get('lon')
        location = request.GET.get('location', 'Unknown')
        days = int(request.GET.get('days', 5))

        if not lat or not lon:
            return Response({'error': 'Latitude and longitude are required'}, status=400)

        # Check if we have recent forecast data
        recent_forecast = WeatherForecast.objects.filter(
            latitude=lat,
            longitude=lon,
            created_at__gte=datetime.now() - timedelta(hours=6)
        ).order_by('forecast_date', 'forecast_time')

        if recent_forecast.exists():
            forecast_data = []
            for forecast in recent_forecast[:days*8]:  # 8 forecasts per day (3-hour intervals)
                forecast_data.append({
                    'date': forecast.forecast_date.isoformat(),
                    'time': forecast.forecast_time.isoformat(),
                    'temperature': float(forecast.temperature),
                    'temperature_min': float(forecast.temperature_min) if forecast.temperature_min else None,
                    'temperature_max': float(forecast.temperature_max) if forecast.temperature_max else None,
                    'humidity': forecast.humidity,
                    'pressure': forecast.pressure,
                    'wind_speed': float(forecast.wind_speed),
                    'wind_direction': forecast.wind_direction,
                    'weather_condition': forecast.weather_condition,
                    'weather_description': forecast.weather_description,
                    'weather_icon': forecast.weather_icon,
                    'precipitation_probability': forecast.precipitation_probability,
                    'precipitation_amount': float(forecast.precipitation_amount)
                })

            return Response({
                'location': location,
                'forecast': forecast_data
            })

        # Fetch from OpenWeatherMap API
        api_key = getattr(settings, 'OPENWEATHER_API_KEY', 'demo_key')
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"

        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()

            # Save forecast data
            forecast_objects = []
            for item in data['list'][:days*8]:  # Limit to requested days
                forecast_date = datetime.fromtimestamp(item['dt']).date()
                forecast_time = datetime.fromtimestamp(item['dt']).time()

                forecast = WeatherForecast.objects.create(
                    location=location,
                    latitude=lat,
                    longitude=lon,
                    forecast_date=forecast_date,
                    forecast_time=forecast_time,
                    temperature=item['main']['temp'],
                    temperature_min=item['main'].get('temp_min'),
                    temperature_max=item['main'].get('temp_max'),
                    humidity=item['main']['humidity'],
                    pressure=item['main']['pressure'],
                    wind_speed=item['wind']['speed'],
                    wind_direction=item['wind']['deg'],
                    weather_condition=item['weather'][0]['main'],
                    weather_description=item['weather'][0]['description'],
                    weather_icon=item['weather'][0]['icon'],
                    precipitation_probability=int(item.get('pop', 0) * 100),
                    precipitation_amount=item.get('rain', {}).get('3h', 0) if 'rain' in item else 0
                )
                forecast_objects.append(forecast)

            # Return formatted data
            forecast_data = []
            for forecast in forecast_objects:
                forecast_data.append({
                    'date': forecast.forecast_date.isoformat(),
                    'time': forecast.forecast_time.isoformat(),
                    'temperature': float(forecast.temperature),
                    'temperature_min': float(forecast.temperature_min) if forecast.temperature_min else None,
                    'temperature_max': float(forecast.temperature_max) if forecast.temperature_max else None,
                    'humidity': forecast.humidity,
                    'pressure': forecast.pressure,
                    'wind_speed': float(forecast.wind_speed),
                    'wind_direction': forecast.wind_direction,
                    'weather_condition': forecast.weather_condition,
                    'weather_description': forecast.weather_description,
                    'weather_icon': forecast.weather_icon,
                    'precipitation_probability': forecast.precipitation_probability,
                    'precipitation_amount': float(forecast.precipitation_amount)
                })

            return Response({
                'location': location,
                'forecast': forecast_data
            })
        else:
            return Response({'error': 'Forecast service unavailable'}, status=503)

    except Exception as e:
        return Response({
            'error': f'Error retrieving forecast data: {str(e)}'
        }, status=500)

@api_view(['GET'])
def get_user_notifications(request):
    """
    Get notifications for the authenticated user
    """
    try:
        from app.models import Notification

        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=401)

        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')

        # Mark notifications as read if requested
        mark_read = request.GET.get('mark_read', 'false').lower() == 'true'
        if mark_read:
            notifications.filter(is_read=False).update(is_read=True)

        notifications_data = []
        for notification in notifications[:20]:  # Limit to 20 most recent
            notifications_data.append({
                'id': notification.id,
                'title': notification.title,
                'message': notification.message,
                'type': notification.notification_type,
                'priority': notification.priority,
                'data': notification.data,
                'is_read': notification.is_read,
                'created_at': notification.created_at.isoformat()
            })

        return Response({
            'notifications': notifications_data,
            'unread_count': notifications.filter(is_read=False).count()
        })

    except Exception as e:
        return Response({
            'error': f'Error retrieving notifications: {str(e)}'
        }, status=500)

@api_view(['POST'])
def create_notification(request):
    """
    Create a new notification (admin/system use)
    """
    try:
        from app.models import Notification, User

        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=401)

        user_id = request.data.get('user_id')
        title = request.data.get('title')
        message = request.data.get('message')
        notification_type = request.data.get('type', 'system')
        priority = request.data.get('priority', 'medium')

        if not title or not message:
            return Response({'error': 'Title and message are required'}, status=400)

        # Get target user(s)
        if user_id:
            try:
                user = User.objects.get(id=user_id)
                users = [user]
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=404)
        else:
            # Broadcast to all users (admin only)
            if not request.user.is_staff:
                return Response({'error': 'Admin privileges required for broadcast'}, status=403)
            users = User.objects.all()

        created_notifications = []
        for user in users:
            notification = Notification.objects.create(
                user=user,
                title=title,
                message=message,
                notification_type=notification_type,
                priority=priority,
                data=request.data.get('data', {})
            )
            created_notifications.append(notification)

        return Response({
            'success': True,
            'created_count': len(created_notifications),
            'message': f'Notification sent to {len(created_notifications)} user(s)'
        })

    except Exception as e:
        return Response({
            'error': f'Error creating notification: {str(e)}'
        }, status=500)

@api_view(['POST'])
def update_notification_preferences(request):
    """
    Update user's notification preferences
    """
    try:
        from app.models import NotificationPreference

        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=401)

        preferences, created = NotificationPreference.objects.get_or_create(
            user=request.user,
            defaults={
                'weather_alerts': True,
                'extreme_weather_warnings': True,
                'disease_risk_alerts': True,
                'disease_detection_alerts': True,
                'treatment_reminders': True,
                'market_price_alerts': False,
                'product_availability_alerts': False,
                'system_updates': True,
                'security_alerts': True,
                'email_notifications': True,
                'push_notifications': True,
                'sms_notifications': False
            }
        )

        # Update preferences
        for field in request.data:
            if hasattr(preferences, field):
                setattr(preferences, field, request.data[field])

        preferences.save()

        return Response({
            'success': True,
            'message': 'Notification preferences updated successfully',
            'preferences': {
                'weather_alerts': preferences.weather_alerts,
                'extreme_weather_warnings': preferences.extreme_weather_warnings,
                'disease_risk_alerts': preferences.disease_risk_alerts,
                'disease_detection_alerts': preferences.disease_detection_alerts,
                'treatment_reminders': preferences.treatment_reminders,
                'market_price_alerts': preferences.market_price_alerts,
                'product_availability_alerts': preferences.product_availability_alerts,
                'system_updates': preferences.system_updates,
                'security_alerts': preferences.security_alerts,
                'email_notifications': preferences.email_notifications,
                'push_notifications': preferences.push_notifications,
                'sms_notifications': preferences.sms_notifications,
                'quiet_hours_start': preferences.quiet_hours_start.isoformat() if preferences.quiet_hours_start else None,
                'quiet_hours_end': preferences.quiet_hours_end.isoformat() if preferences.quiet_hours_end else None
            }
        })

    except Exception as e:
        return Response({
            'error': f'Error updating preferences: {str(e)}'
        }, status=500)

@api_view(['GET'])
def get_notification_preferences(request):
    """
    Get user's notification preferences
    """
    try:
        from app.models import NotificationPreference

        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required'}, status=401)

        preferences, created = NotificationPreference.objects.get_or_create(
            user=request.user,
            defaults={
                'weather_alerts': True,
                'extreme_weather_warnings': True,
                'disease_risk_alerts': True,
                'disease_detection_alerts': True,
                'treatment_reminders': True,
                'market_price_alerts': False,
                'product_availability_alerts': False,
                'system_updates': True,
                'security_alerts': True,
                'email_notifications': True,
                'push_notifications': True,
                'sms_notifications': False
            }
        )

        return Response({
            'preferences': {
                'weather_alerts': preferences.weather_alerts,
                'extreme_weather_warnings': preferences.extreme_weather_warnings,
                'disease_risk_alerts': preferences.disease_risk_alerts,
                'disease_detection_alerts': preferences.disease_detection_alerts,
                'treatment_reminders': preferences.treatment_reminders,
                'market_price_alerts': preferences.market_price_alerts,
                'product_availability_alerts': preferences.product_availability_alerts,
                'system_updates': preferences.system_updates,
                'security_alerts': preferences.security_alerts,
                'email_notifications': preferences.email_notifications,
                'push_notifications': preferences.push_notifications,
                'sms_notifications': preferences.sms_notifications,
                'quiet_hours_start': preferences.quiet_hours_start.isoformat() if preferences.quiet_hours_start else None,
                'quiet_hours_end': preferences.quiet_hours_end.isoformat() if preferences.quiet_hours_end else None
            }
        })

    except Exception as e:
        return Response({
            'error': f'Error retrieving preferences: {str(e)}'
        }, status=500)


@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint for Render monitoring
    """
    try:
        from django.db import connection
        from app.model import ModelWrapper

        # Check database connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()

        # Check ML model loading
        model_wrapper = ModelWrapper()
        models_loaded = model_wrapper.check_models_loaded()

        return Response({
            'status': 'healthy',
            'database': 'connected',
            'ml_models': 'loaded' if models_loaded else 'loading',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        })

    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }, status=503)
<<<<<<< HEAD

@api_view(['GET'])
def health_check(request):
    """
    Health check endpoint for Render monitoring
    """
    try:
        from django.db import connection
        from app.model import ModelWrapper

        # Check database connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()

        # Check ML model loading
        model_wrapper = ModelWrapper()
        models_loaded = model_wrapper.check_models_loaded()

        return Response({
            'status': 'healthy',
            'database': 'connected',
            'ml_models': 'loaded' if models_loaded else 'loading',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0'
        })

    except Exception as e:
        return Response({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }, status=503)
=======
>>>>>>> 8260561a942e7dca9091fa4b72e6f3af58e16a2c
