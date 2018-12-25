"""
Test Tasks
"""

from celery import shared_task
import time


@shared_task
def hello(text):
    return {"status": "passed", "result": text}


@shared_task
def non_blocking_call(hold_on):
    try:
        time.sleep(hold_on)
        return {"status": "passed", "result": "{}", "notify_type": "passed"}
    except Exception as e:
        return {
            "status": "failed",
            "result": {
                "error": str(e)
            },
            "notify_type": "error"
        }
