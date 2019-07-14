"""
Verify Subscription Tasks
"""

# Third Party Library
from celery import shared_task


@shared_task
def verify_subscriber_email():
    pass


@shared_task
def verify_subscriber_phone():
    pass


@shared_task
def verify_subscriber_endpoint():
    pass
