from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
import random
from datetime import datetime, timedelta


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def predict_disease(request):
    """
    Predict crop disease from uploaded leaf image
    Currently returns mock data - will be replaced with actual ML model
    """
    if 'image' not in request.FILES:
        return Response(
            {'error': 'No image file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Mock prediction response
    diseases = [
        'Healthy',
        'Early Blight',
        'Late Blight',
        'Leaf Spot',
        'Powdery Mildew',
        'Rust',
    ]
    
    prediction = random.choice(diseases)
    confidence = round(random.uniform(0.75, 0.99), 2)
    
    # Mock recommendations
    recommendations = {
        'Healthy': 'Your crop appears healthy! Continue with regular monitoring.',
        'Early Blight': 'Apply fungicide and remove affected leaves. Ensure proper spacing for air circulation.',
        'Late Blight': 'Remove infected plants immediately. Apply copper-based fungicide.',
        'Leaf Spot': 'Improve air circulation and avoid overhead watering. Apply appropriate fungicide.',
        'Powdery Mildew': 'Spray with neem oil or sulfur-based fungicide. Improve air flow.',
        'Rust': 'Remove infected leaves and apply rust fungicide. Practice crop rotation.',
    }
    
    response_data = {
        'disease': prediction,
        'confidence': confidence,
        'severity': 'Low' if prediction == 'Healthy' else random.choice(['Low', 'Medium', 'High']),
        'recommendation': recommendations.get(prediction, 'Consult agricultural expert'),
        'timestamp': datetime.now().isoformat(),
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recommend_crop(request):
    """
    Recommend suitable crops based on soil and climate data
    Currently returns mock data - will be replaced with actual ML model
    """
    # Expected input: soil_type, rainfall, temperature, ph_level
    soil_type = request.data.get('soil_type')
    rainfall = request.data.get('rainfall')
    temperature = request.data.get('temperature')
    
    if not all([soil_type, rainfall, temperature]):
        return Response(
            {'error': 'Missing required parameters: soil_type, rainfall, temperature'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Mock crop recommendations
    crops = [
        {
            'name': 'Maize',
            'suitability_score': round(random.uniform(0.7, 0.95), 2),
            'expected_yield': f'{random.randint(20, 40)} bags/acre',
            'growing_period': '3-4 months',
            'water_requirement': 'Medium',
        },
        {
            'name': 'Beans',
            'suitability_score': round(random.uniform(0.7, 0.95), 2),
            'expected_yield': f'{random.randint(8, 15)} bags/acre',
            'growing_period': '2-3 months',
            'water_requirement': 'Low',
        },
        {
            'name': 'Tomatoes',
            'suitability_score': round(random.uniform(0.7, 0.95), 2),
            'expected_yield': f'{random.randint(150, 300)} crates/acre',
            'growing_period': '3-4 months',
            'water_requirement': 'High',
        },
    ]
    
    # Sort by suitability score
    crops.sort(key=lambda x: x['suitability_score'], reverse=True)
    
    response_data = {
        'location': request.data.get('location', 'Not specified'),
        'soil_type': soil_type,
        'recommendations': crops,
        'timestamp': datetime.now().isoformat(),
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def climate_forecast(request):
    """
    Provide climate forecast for agricultural planning
    Currently returns mock data - will be replaced with actual ML model
    """
    location = request.data.get('location')
    days = request.data.get('days', 7)
    
    if not location:
        return Response(
            {'error': 'Location parameter is required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Generate mock forecast data
    forecast = []
    base_temp = random.randint(18, 28)
    
    for i in range(int(days)):
        date = datetime.now() + timedelta(days=i)
        forecast.append({
            'date': date.strftime('%Y-%m-%d'),
            'temperature': {
                'min': base_temp + random.randint(-3, 0),
                'max': base_temp + random.randint(5, 10),
                'avg': base_temp + random.randint(2, 5),
            },
            'rainfall': round(random.uniform(0, 15), 1),
            'humidity': random.randint(60, 90),
            'wind_speed': round(random.uniform(5, 20), 1),
            'description': random.choice(['Sunny', 'Partly Cloudy', 'Cloudy', 'Rainy', 'Thunderstorms']),
        })
    
    response_data = {
        'location': location,
        'forecast_period': f'{days} days',
        'forecast': forecast,
        'agricultural_advice': 'Plan irrigation accordingly based on rainfall forecast.',
        'timestamp': datetime.now().isoformat(),
    }
    
    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ml_status(request):
    """Check ML service status"""
    return Response({
        'status': 'operational',
        'models': {
            'disease_detection': 'mock',
            'crop_recommendation': 'mock',
            'climate_forecast': 'mock',
        },
        'message': 'ML endpoints are operational with mock data. Real models will be integrated on Day 3.',
    })