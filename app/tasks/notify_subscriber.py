"""
Notify Subscriber Tasks
"""

# Third party
from celery import shared_task
from app.modules.core.incident_update import Incident_Update as Incident_Update_Module
from app.modules.core.incident_update_notification import Incident_Update_Notification as Incident_Update_Notification_Module


@shared_task
def notify_subscriber(notification_id):

    incident_update_notification_module = Incident_Update_Notification_Module()
    incident_update_module = Incident_Update_Module()

    notification = incident_update_notification_module.get_one_by_id(notification_id)
    incident_update = incident_update_module.get_one_by_id(notification["incident_update"].id)

    if notification["status"] == "pending":
        status = True
        if status:
            # message sent
            incident_update_notification_module.update_one_by_id(notification["id"], {
                "status": "success"
            })
            incident_update_module.update_one_by_id(incident_update["id"], {
                "notified_subscribers": incident_update["notified_subscribers"] + 1
            })

        else:
            # message failed
            incident_update_notification_module.update_one_by_id(notification["id"], {
                "status": "failed"
            })
            incident_update_module.update_one_by_id(incident_update["id"], {
                "failed_subscribers": incident_update["failed_subscribers"] - 1
            })

    elif notification["status"] == "failed":
        status = True
        if status:
            # message sent again
            incident_update_notification_module.update_one_by_id(notification["id"], {
                "status": "success"
            })
            incident_update_module.update_one_by_id(incident_update["id"], {
                "notified_subscribers": incident_update.notified_subscribers + 1,
                "failed_subscribers": incident_update["failed_subscribers"] - 1
            })

    return {
        "status": "passed",
        "result": "{}",
        "notify_type": "passed"
    }
