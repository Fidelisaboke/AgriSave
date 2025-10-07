from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Crop, WeatherData, GreenPoint

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile with nested user data"""
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'phone_number', 'location', 'farm_size',
            'total_green_points', 'badge_tier', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'total_green_points', 'badge_tier', 'created_at', 'updated_at']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration"""
    password = serializers.CharField(write_only=True, min_length=8)
    password2 = serializers.CharField(write_only=True, min_length=8)
    phone_number = serializers.CharField(required=False)
    location = serializers.CharField(required=True)
    farm_size = serializers.DecimalField(max_digits=10, decimal_places=2, required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'first_name', 
                  'last_name', 'phone_number', 'location', 'farm_size']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords don't match")
        return data
    
    def create(self, validated_data):
        # Remove profile-related fields
        phone_number = validated_data.pop('phone_number', None)
        location = validated_data.pop('location')
        farm_size = validated_data.pop('farm_size')
        validated_data.pop('password2')
        
        # Create user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        
        # Create profile
        UserProfile.objects.create(
            user=user,
            phone_number=phone_number,
            location=location,
            farm_size=farm_size
        )
        
        return user


class CropSerializer(serializers.ModelSerializer):
    """Serializer for Crop model"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = Crop
        fields = [
            'id', 'user', 'user_username', 'name', 'crop_type', 'variety',
            'planting_date', 'expected_harvest_date', 'area_planted', 'status',
            'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        # Automatically set user from request context
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)


class GreenPointSummarySerializer(serializers.Serializer):
    """Serializer for Green Points summary"""
    total_points = serializers.IntegerField()
    badge_tier = serializers.CharField()
    recent_activities = serializers.ListField(child=serializers.DictField(), required=False)
    points_to_next_tier = serializers.IntegerField()
    next_tier = serializers.CharField()


class WeatherDataSerializer(serializers.ModelSerializer):
    """Serializer for WeatherData model"""
    
    class Meta:
        model = WeatherData
        fields = [
            'id', 'location', 'latitude', 'longitude', 'temperature',
            'humidity', 'rainfall', 'wind_speed', 'pressure', 'description',
            'recorded_at', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class GreenPointSerializer(serializers.ModelSerializer):
    """Serializer for GreenPoint model"""
    user_username = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = GreenPoint
        fields = [
            'id', 'user', 'user_username', 'activity_type', 'description',
            'points_earned', 'verified', 'verification_date', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'points_earned', 'created_at']
    
    def create(self, validated_data):
        # Automatically set user from request context
        user = self.context['request'].user
        validated_data['user'] = user