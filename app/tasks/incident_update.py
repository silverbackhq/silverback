"""
Incident Update Tasks
"""

# Third party
from celery import shared_task
from app.modules.core.task import Task as Task_Module
from app.modules.core.incident_update_notification import Incident_Update_Notification as Incident_Update_Notification_Module
from app.modules.core.subscriber import Subscriber as Subscriber_Module


@shared_task
def incident_update(incident_update_id, user_id):

    incident_update_notification_module = Incident_Update_Notification_Module()
    subscriber_module = Subscriber_Module()
    task_module = Task_Module()

    for subscriber in subscriber_module.get_iterator():
        notification = incident_update_notification_module.is_subscriber_notified(
            incident_update_id,
            subscriber.id
        )
        if notification:
            if notification.status == "failed":
                # Update as Pending and send to queue
                result = incident_update_notification_module.update_one_by_id(notification.id, {
                    "status": "pending"
                })

                if result:
                    # Send notification.id to the Queue
                    task_module.delay("notify_subscriber", {
                        "notification_id": notification.id
                    }, user_id)

            elif notification.status == "pending":
                # Send notification.id to the Queue
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
