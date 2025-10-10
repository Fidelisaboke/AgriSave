from django.core.management.base import BaseCommand
from ml_engine.pipelines.crop_recommendation import run_crop_recommendation_training


class Command(BaseCommand):
    """
    A Django management command to run the disease detection model training pipeline.
    """
    help = 'Starts the training and evaluation process for the crop recommendation model.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting Crop Recommendation Model Training Pipeline..."))

        try:
            run_crop_recommendation_training()
            self.stdout.write(self.style.SUCCESS("Training pipeline completed successfully!"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred during training: {e}"))
