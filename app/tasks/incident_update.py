"""
Incident Update Tasks
"""

# Third Party Library
from celery import shared_task

# Local Library
from app.modules.core.task import Task as TaskModule
from app.modules.core.subscriber import Subscriber as SubscriberModule
from app.modules.core.incident_update_notification import IncidentUpdateNotification as IncidentUpdateNotificationModule


@shared_task
def incident_update(incident_update_id, user_id):

    incident_update_notification_module = IncidentUpdateNotificationModule()
    subscriber_module = SubscriberModule()
    task_module = TaskModule()

    for subscriber in subscriber_module.get_iterator():
        notification = incident_update_notification_module.is_subscriber_notified(
            incident_update_id,
            subscriber.id
        )
        if notification:
            # Send notification.id to the queue again
            task_module.delay("notify_subscriber", {
                "notification_id": notification.id
            }, user_id)

        else:
            # Create new notification and send to queue
            new_notification = incident_update_notification_module.insert_one({
                "status": "pending",
                "incident_update_id": incident_update_id,
                "subscriber_id": subscriber.id
            })
            if new_notification:
                # Send new_notification.id to the Queue
                task_module.delay("notify_subscriber", {
                    "notification_id": new_notification.id
                }, user_id)

    return {
        "status": "passed",
        "result": "{}",
        "notify_type": "passed"
    }
