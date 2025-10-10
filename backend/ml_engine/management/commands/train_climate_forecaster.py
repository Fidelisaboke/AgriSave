from django.core.management.base import BaseCommand
from ml_engine.pipelines.climate_forecasting import run_climate_forecasting_training


class Command(BaseCommand):
    """
    A Django management command to run the climate forecasting model training pipeline.
    """
    help = 'Starts the training and evaluation process for the climate forecasting model.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting Climate Forecasting Model Training Pipeline..."))

        try:
            run_climate_forecasting_training()
            self.stdout.write(self.style.SUCCESS("Training pipeline completed successfully!"))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"An error occurred during training: {e}"))
