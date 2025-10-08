from django.contrib import admin
from .models import UserProfile, Crop, WeatherData, GreenPoint


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'location', 'farm_size', 'total_green_points', 'badge_tier', 'created_at']
    list_filter = ['badge_tier', 'created_at']
    search_fields = ['user__username', 'user__email', 'location']
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['name', 'crop_type', 'user', 'status', 'planting_date', 'expected_harvest_date']
    list_filter = ['crop_type', 'status', 'planting_date']
    search_fields = ['name', 'user__username', 'variety']
    date_hierarchy = 'planting_date'
    readonly_fields = ['created_at', 'updated_at']


@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['location', 'temperature', 'humidity', 'rainfall', 'recorded_at']
    list_filter = ['recorded_at', 'location']
    search_fields = ['location', 'description']
    date_hierarchy = 'recorded_at'
    readonly_fields = ['created_at']


@admin.register(GreenPoint)
class GreenPointAdmin(admin.ModelAdmin):
    list_display = ['user', 'activity_type', 'points_earned', 'verified', 'created_at']
    list_filter = ['activity_type', 'verified', 'created_at']
    search_fields = ['user__username', 'description']
    date_hierarchy = 'created_at'
    actions = ['verify_activities']
    
    def verify_activities(self, request, queryset):
        from django.utils import timezone
        updated = queryset.update(verified=True, verification_date=timezone.now())
        self.message_user(request, f'{updated} activities verified successfully.')
    verify_activities.short_description = 'Verify selected activities'