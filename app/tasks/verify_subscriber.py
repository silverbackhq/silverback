"""
Verify Subscriber Tasks
"""

# Third Party Library
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string


@shared_task
def verify_email():
    pass


@shared_task
def verify_phone():
    pass


@shared_task
def verify_endpoint():
    pass
