"""
Celery Configs
"""

# standard library
import os
from importlib import import_module

# Third party
from celery import Celery
from celery.signals import task_success

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings.basic")

app = Celery('app')

# namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@task_success.connect
def after_task(sender=None, result=None, **kwargs):
    if sender.request.id and "status" in result and "result" in result:
        task_module = import_module("app.modules.core.task")
        task_class = getattr(task_module, "Task")

        notification_module = import_module("app.modules.core.notification")
        notification_class = getattr(notification_module, "Notification")

        task_class().update_task_with_uuid(
            sender.request.id,
            {
                "status": result["status"],
                "result": result["result"]
            }
        )

        task = task_class().get_task_with_uuid(sender.request.id)

        if task and "notify_type" in result:
            notification_class().update_task_notification(
                task.id,
                result["notify_type"]
            )
