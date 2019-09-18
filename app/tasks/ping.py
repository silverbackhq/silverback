"""
    Test Tasks
    ~~~~~~~~~~~~~~

    :copyright: silverbackhq
    :license: BSD-3-Clause
"""

# Third Party Library
from celery import shared_task


@shared_task
def ping(text="PONG"):
    return {"status": "passed", "result": text}
