from django.core.management.base import BaseCommand
from apps.ml_engine.pipelines.disease_detection import run_disease_detection_training


class Command(BaseCommand):
    """
    A Django management command to run the disease detection model training pipeline.
    """
    help = 'Starts the training and evaluation process for the disease detection model.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting Disease Detection Model Training Pipeline..."))

        try:
            run_disease_detection_training()
            self.stdout.write(self.style.SUCCESS("Training pipeline completed successfully!"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred during training: {e}"))
