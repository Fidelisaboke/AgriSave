from django.core.management.base import BaseCommand
from django.db import transaction
from django.contrib.auth import get_user_model
from apps.core_api.models import GreenPoint, UserProfile
import threading

class Command(BaseCommand):
    help = 'Test for race conditions in GreenPoint verification'

    def handle(self, *args, **options):
        def verify_green_point(greenpoint_id, points, results, index):
            """Thread function to verify a green point"""
            try:
                # This simulates the actual verification process in the model
                with transaction.atomic():
                    point = GreenPoint.objects.select_for_update().get(pk=greenpoint_id)
                    if not point.verified:
                        # Instead of saving directly, we'll call the save method to trigger the logic
                        point.verified = True
                        # Save without specifying fields to ensure the save method runs fully
                        point.save()
                        results[index] = f"Success - Added {points} points"
                    else:
                        results[index] = "Already verified"
            except Exception as e:
                results[index] = f"Error: {str(e)}"

        # Setup test user and points
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username='test_race_user',
            defaults={'email': 'test_race@example.com', 'password': 'testpass123'}
        )
        
        if created:
            UserProfile.objects.create(user=user, location='Test Location', farm_size=1.0)
        
        profile = user.profile
        
        # Reset test data
        profile.total_green_points = 0
        profile.badge_tier = 'bronze'
        profile.save()
        user.green_points.all().delete()
        
        # Create multiple green points for the same user
        points = [10, 15, 20, 25, 30]
        greenpoints = []
        for point in points:
            gp = GreenPoint.objects.create(
                user=user,
                activity_type='recycling',
                description=f'Test point worth {point} points',
                points_earned=point,
                verified=False
            )
            greenpoints.append(gp)
        
        # Verify points in parallel
        threads = []
        results = [None] * len(greenpoints)
        
        self.stdout.write(self.style.SUCCESS("Starting concurrent verification..."))
        for i, gp in enumerate(greenpoints):
            # Refresh the point to ensure we have the latest version
            gp.refresh_from_db()
            t = threading.Thread(
                target=verify_green_point,
                args=(gp.id, gp.points_earned, results, i)
            )
            threads.append(t)
            t.start()
        
        # Wait for all threads to complete
        for t in threads:
            t.join()
            
        # Ensure all points are verified and processed
        for gp in greenpoints:
            gp.refresh_from_db()
        profile.refresh_from_db()
        
        # Print results
        self.stdout.write("\nVerification results:")
        for i, result in enumerate(results):
            self.stdout.write(f"Point {i+1} ({points[i]}): {result}")
        
        # Check final points
        profile.refresh_from_db()
        expected_points = sum(points)
        
        self.stdout.write(f"\nExpected total points: {expected_points}")
        self.stdout.write(f"Actual total points: {profile.total_green_points}")
        self.stdout.write(f"Badge tier: {profile.badge_tier}")
        
        # Assert the test passed
        if profile.total_green_points == expected_points:
            self.stdout.write(
                self.style.SUCCESS("\n✅ Test passed - No race conditions detected!")
            )
            return
            
        self.stdout.write(
            self.style.ERROR(
                f"\n❌ Race condition detected! Expected {expected_points} points, "
                f"got {profile.total_green_points}"
            )
        )
