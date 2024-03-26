# tasks.py

from celery import shared_task

@shared_task
def my_background_task():
    result  = 5
    return result
