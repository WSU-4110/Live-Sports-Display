# tasks.py

from celery import shared_task
import logging

logger = logging.getLogger(__name__)
@shared_task
def my_background_task():
    logger.info('Running the asynchronous task...')
    result  = 5
    return result
