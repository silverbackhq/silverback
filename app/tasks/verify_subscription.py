"""
    Verify Subscription Tasks
    ~~~~~~~~~~~~~~

    :copyright: silverbackhq
    :license: BSD-3-Clause
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
