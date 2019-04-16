"""
Test Tasks
"""

from celery import shared_task


@shared_task
def ping(text="PONG"):
    return {"status": "passed", "result": text}
