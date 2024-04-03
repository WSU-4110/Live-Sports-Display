from celery import shared_task
from .SSH import run_stacked_display  # Ensure this import is correct

@shared_task
def my_background_task():
    run_stacked_display()
    return "Completed"
