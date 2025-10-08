from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class UserProfile(models.Model):
    """Extended user profile for farmers"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    location = models.CharField(max_length=200)
    farm_size = models.DecimalField(max_digits=10, decimal_places=2, help_text="Farm size in acres")
    total_green_points = models.IntegerField(default=0)
    badge_tier = models.CharField(
        max_length=20,
        choices=[
            ('bronze', 'Bronze'),
            ('silver', 'Silver'),
            ('gold', 'Gold'),
            ('platinum', 'Platinum')
        ],
        default='bronze'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.location}"

    class Meta:
        ordering = ['-created_at']


class Crop(models.Model):
    """Crop information and management"""
    CROP_TYPES = [
        ('cereals', 'Cereals'),
        ('vegetables', 'Vegetables'),
        ('fruits', 'Fruits'),
        ('legumes', 'Legumes'),
        ('tubers', 'Tubers'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='crops')
    name = models.CharField(max_length=100)
    crop_type = models.CharField(max_length=20, choices=CROP_TYPES)
    variety = models.CharField(max_length=100, blank=True)
    planting_date = models.DateField()
    expected_harvest_date = models.DateField()
    area_planted = models.DecimalField(max_digits=10, decimal_places=2, help_text="Area in acres")
    status = models.CharField(
        max_length=20,
        choices=[
            ('planted', 'Planted'),
            ('growing', 'Growing'),
            ('harvested', 'Harvested'),
            ('failed', 'Failed')
        ],
        default='planted'
    )
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.crop_type}) - {self.user.username}"

    class Meta:
        ordering = ['-planting_date']


class WeatherData(models.Model):
    """Store weather information for analysis"""
    location = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    temperature = models.DecimalField(max_digits=5, decimal_places=2, help_text="Temperature in Celsius")
    humidity = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Humidity percentage"
    )
    rainfall = models.DecimalField(max_digits=6, decimal_places=2, help_text="Rainfall in mm")
    wind_speed = models.DecimalField(max_digits=5, decimal_places=2, help_text="Wind speed in km/h")
    pressure = models.DecimalField(max_digits=7, decimal_places=2, help_text="Pressure in hPa")
    description = models.CharField(max_length=200)
    recorded_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.location} - {self.recorded_at.strftime('%Y-%m-%d %H:%M')}"

    class Meta:
        ordering = ['-recorded_at']
        verbose_name_plural = "Weather Data"


class GreenPoint(models.Model):
    """Track sustainability activities and points"""
    ACTIVITY_TYPES = [
        ('intercropping', 'Intercropping'),
        ('organic', 'Organic Farming'),
        ('recycling', 'Recycling'),
        ('water_conservation', 'Water Conservation'),
        ('composting', 'Composting'),
        ('renewable_energy', 'Renewable Energy'),
    ]
    
    POINT_VALUES = {
        'intercropping': 10,
        'organic': 15,
        'recycling': 20,
        'water_conservation': 15,
        'composting': 12,
        'renewable_energy': 25,
    }
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='green_points')
    activity_type = models.CharField(max_length=30, choices=ACTIVITY_TYPES)
    description = models.TextField()
    points_earned = models.IntegerField(default=0)
    verified = models.BooleanField(default=False)
    verification_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        from django.db import transaction
        from django.db.models import F
        
        # Auto-assign points based on activity type if not set
        if not self.points_earned:
            self.points_earned = self.POINT_VALUES.get(self.activity_type, 0)
        
        # Get the original verified state before saving
        if self.pk:
            try:
                original = type(self).objects.get(pk=self.pk)
                self._original_verified = original.verified
            except type(self).DoesNotExist:
                self._original_verified = False
        else:
            self._original_verified = False
            
        # Check if this is a new verification
        is_new_verification = (not self._original_verified and self.verified)
        
        # Save the GreenPoint instance
        with transaction.atomic():
            super().save(*args, **kwargs)
            
            # If this is a new verification, update the user's points
            if is_new_verification:
                
                # Use select_for_update to lock the profile row during the update
                profile = (
                    UserProfile.objects
                    .select_for_update()
                    .get(user=self.user)
                )
                
                # Calculate new points and update in a single operation
                new_points = profile.total_green_points + self.points_earned
                
                # Determine new badge tier
                if new_points >= 500:
                    new_tier = 'platinum'
                elif new_points >= 300:
                    new_tier = 'gold'
                elif new_points >= 150:
                    new_tier = 'silver'
                else:
                    new_tier = 'bronze'
                
                # Update both fields in a single save
                UserProfile.objects.filter(pk=profile.pk).update(
                    total_green_points=new_points,
                    badge_tier=new_tier
                )

    def __str__(self):
        return f"{self.user.username} - {self.activity_type} ({self.points_earned} pts)"

    class Meta:
        ordering = ['-created_at']