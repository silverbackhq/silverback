"""
Notify Subscriber Tasks
"""

# Third party
from celery import shared_task


@shared_task
def notify_subscriber(app_name, app_email, app_url):
    return {
        "status": "passed",
        "result": "{}"
    }
