"""
Incident Update Tasks
"""

# Third party
from celery import shared_task


@shared_task
def incident_update(incident_update_id):
    return {
        "status": "passed",
        "result": "{}",
        "notify_type": "passed"
    }
