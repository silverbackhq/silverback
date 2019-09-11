"""
Verify Subscriber Tasks
"""

# Third Party Library
from celery import shared_task


@shared_task
def verify_email():
    pass


@shared_task
def verify_phone():
    pass


@shared_task
def verify_endpoint():
    pass
