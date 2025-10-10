import logging

from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime

from .apps import MlEngineConfig
from .serializers import CropRecommendationSerializer
from .services import inference

logger = logging.getLogger(__name__)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def predict_disease(request):
    """
    Predict crop disease from uploaded leaf image.
    """
    image_file = request.FILES.get('image')
    if not image_file:
        return Response(
            {'error': 'No image file provided'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        prediction_result = inference.predict_disease(image_file)
        disease_name = prediction_result.get('disease', 'Unknown')

        # TODO: Add recommendations based on the predicted class

        response_data = {
            'disease': disease_name.replace('___', ' ').replace('_', ' '),
            'confidence': prediction_result.get('confidence', 0.0),
            'timestamp': datetime.now().isoformat(),
        }

        return Response(response_data, status=status.HTTP_200_OK)

    except RuntimeError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except Exception as e:
        logging.error(f"Unexpected error in predict_disease: {e}")
        return Response(
            {'error': 'An unexpected error occurred.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recommend_crop(request):
    """
    Recommend suitable crops based on soil and climate data.
    """
    serializer = CropRecommendationSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        prediction_result = inference.recommend_crop(serializer.validated_data)

        response_data = {
            'inputs': serializer.validated_data,
            'prediction': prediction_result,
            'timestamp': datetime.now().isoformat(),
        }
        return Response(response_data, status=status.HTTP_200_OK)

    except RuntimeError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_503_SERVICE_UNAVAILABLE
        )
    except Exception as e:
        logger.error(f"Unexpected error in recommend_crop: {e}")
        return Response(
            {'error': 'An unexpected error occurred.'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def climate_forecast(request):
    """
    Provide climate forecast for agricultural planning.
    NOTE: This requires fetching historical data to feed the model.
    """
    location = request.data.get('location')
    if not location:
        return Response({'error': 'Location parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Placeholder response until data fetching is implemented
        return Response({
            'message': 'Climate forecast endpoint is connected, but historical data fetching is not yet implemented.',
            'required_input_shape': '(14, 5)',  # Example shape
        }, status=status.HTTP_200_OK)

    except RuntimeError as e:
        return Response({'error': str(e)}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as e:
        logger.error(f"Unexpected error in climate_forecast: {e}")
        return Response(
            {'error': 'An unexpected error occurred'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ml_status(request):
    """
    Check the live status of the loaded ML models.
    """
    registry = MlEngineConfig.REGISTRY

    status_report = {
        'disease_detection': 'loaded' if 'disease_model' in registry else 'not_loaded',
        'crop_recommendation': 'loaded' if 'crop_model' in registry else 'not_loaded',
        'climate_forecasting': 'loaded' if 'climate_model' in registry else 'not_loaded',
    }

    return Response({
        'status': 'operational',
        'models': status_report
    })
