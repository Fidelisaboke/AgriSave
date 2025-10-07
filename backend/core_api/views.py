from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

from .models import UserProfile, Crop, WeatherData, GreenPoint
from .serializers import (
    UserProfileSerializer, UserRegistrationSerializer, CropSerializer,
    WeatherDataSerializer, GreenPointSerializer, GreenPointSummarySerializer
)


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    """Register a new user with profile"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'User registered successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def current_user(request):
    """Get current authenticated user profile"""
    try:
        profile = request.user.profile
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)
    except UserProfile.DoesNotExist:
        return Response(
            {'error': 'User profile not found'},
            status=status.HTTP_404_NOT_FOUND
        )


class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for UserProfile CRUD operations"""
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own profile
        return UserProfile.objects.filter(user=self.request.user)


class CropViewSet(viewsets.ModelViewSet):
    """ViewSet for Crop CRUD operations"""
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own crops
        return Crop.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get crop statistics for current user"""
        crops = self.get_queryset()
        
        stats = {
            'total_crops': crops.count(),
            'by_status': {},
            'by_type': {},
            'total_area': 0,
        }
        
        for crop in crops:
            # Count by status
            stats['by_status'][crop.status] = stats['by_status'].get(crop.status, 0) + 1
            # Count by type
            stats['by_type'][crop.crop_type] = stats['by_type'].get(crop.crop_type, 0) + 1
            # Sum area
            stats['total_area'] += float(crop.area_planted)
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def upcoming_harvest(self, request):
        """Get crops with upcoming harvest in next 30 days"""
        today = timezone.now().date()
        thirty_days = today + timedelta(days=30)
        
        upcoming = self.get_queryset().filter(
            expected_harvest_date__gte=today,
            expected_harvest_date__lte=thirty_days,
            status__in=['planted', 'growing']
        )
        
        serializer = self.get_serializer(upcoming, many=True)
        return Response(serializer.data)


class WeatherDataViewSet(viewsets.ModelViewSet):
    """ViewSet for WeatherData CRUD operations"""
    queryset = WeatherData.objects.all()
    serializer_class = WeatherDataSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = WeatherData.objects.all()
        
        # Filter by location if provided
        location = self.request.query_params.get('location', None)
        if location:
            queryset = queryset.filter(location__icontains=location)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        
        if start_date:
            queryset = queryset.filter(recorded_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(recorded_at__lte=end_date)
        
        return queryset
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Get latest weather data for a location"""
        location = request.query_params.get('location')
        if not location:
            return Response(
                {'error': 'Location parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        weather = WeatherData.objects.filter(
            location__icontains=location
        ).order_by('-recorded_at').first()
        
        if weather:
            serializer = self.get_serializer(weather)
            return Response(serializer.data)
        
        return Response(
            {'error': 'No weather data found for this location'},
            status=status.HTTP_404_NOT_FOUND
        )


class GreenPointViewSet(viewsets.ModelViewSet):
    """ViewSet for GreenPoint CRUD operations"""
    queryset = GreenPoint.objects.all()
    serializer_class = GreenPointSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        # Users can only see their own green points
        # Handle schema generation and unauthenticated users
        if getattr(self, 'swagger_fake_view', False):
            return GreenPoint.objects.none()
            
        if not self.request.user.is_authenticated:
            return GreenPoint.objects.none()
            
        return GreenPoint.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get green points summary for current user"""
        user = request.user
        profile = user.profile
        
        # Get recent verified activities
        recent_activities = GreenPoint.objects.filter(
            user=user,
            verified=True
        ).order_by('-created_at')[:5]
        
        # Calculate points to next tier
        tier_thresholds = {
            'bronze': 0,
            'silver': 150,
            'gold': 300,
            'platinum': 500,
        }
        
        current_points = profile.total_green_points
        current_tier = profile.badge_tier
        
        # Find next tier
        next_tier = None
        points_to_next = 0
        
        tier_order = ['bronze', 'silver', 'gold', 'platinum']
        current_index = tier_order.index(current_tier)
        
        if current_index < len(tier_order) - 1:
            next_tier = tier_order[current_index + 1]
            points_to_next = tier_thresholds[next_tier] - current_points
        else:
            next_tier = 'Max tier reached'
            points_to_next = 0
        
        data = {
            'total_points': current_points,
            'badge_tier': current_tier,
            'recent_activities': GreenPointSerializer(recent_activities, many=True).data,
            'points_to_next_tier': points_to_next,
            'next_tier': next_tier,
        }
        
        return Response(data)
    
    @action(detail=True, methods=['post'])
    def verify(self, request, pk=None):
        """Verify a green point activity (admin only)"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admins can verify activities'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        green_point = self.get_object()
        green_point.verified = True
        green_point.verification_date = timezone.now()
        green_point.save()
        
        serializer = self.get_serializer(green_point)
        return Response(serializer.data)