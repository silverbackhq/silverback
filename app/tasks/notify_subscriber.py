"""
Notify Subscriber Tasks
"""

# Django
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext as _

# Third party
import requests
from celery import shared_task
from app.modules.entity.option_entity import Option_Entity
from app.modules.core.incident_update_notification import Incident_Update_Notification as Incident_Update_Notification_Module
from app.modules.core.subscriber import Subscriber as Subscriber_Module


@shared_task
def notify_subscriber(notification_id):

    option_entity = Option_Entity()
    incident_update_notification_module = Incident_Update_Notification_Module()

    app_name = option_entity.get_value_by_key("app_name")
    app_email = option_entity.get_value_by_key("app_email")
    app_url = option_entity.get_value_by_key("app_url")

    notification = incident_update_notification_module.get_one_by_id(notification_id)
    incident_update = notification["incident_update"]
    incident = notification["incident_update"].incident
    subscriber = notification["subscriber"]

    if notification["status"] == "pending":
        # send the notification for the first time
        if subscriber.type == Subscriber_Module.EMAIL:
            status = __deliver_email(
                app_name,
                app_email,
                app_url,
                [subscriber.email],
                _("%s Incident Update: %s") % (app_name, incident.name),
                "mails/incident_update.html",
                {
                    "notification": notification,
                    "incident_update": incident_update,
                    "incident": incident,
                    "subscriber": subscriber
                },
                False
            )
        elif subscriber.type == Subscriber_Module.PHONE:
            status = __deliver_sms(
                subscriber.phone,
                ""
            )
        elif subscriber.type == Subscriber_Module.ENDPOINT:
            status = __deliver_webhook(
                subscriber.endpoint,
                subscriber.auth_token,
                '{}' % ()
            )

        if status:
            # message sent
            incident_update_notification_module.update_one_by_id(notification["id"], {
                "status": "success"
            })

        else:
            # message failed
            incident_update_notification_module.update_one_by_id(notification["id"], {
                "status": "failed"
            })

    elif notification["status"] == "failed":
        # Retry to send the notification
        if subscriber.type == Subscriber_Module.EMAIL:
            status = __deliver_email(
                app_name,
                app_email,
                app_url,
                [subscriber.email],
                _("%s Incident Update: %s") % (app_name, incident.name),
                "mails/incident_update.html",
                {
                    "notification": notification,
                    "incident_update": incident_update,
                    "incident": incident,
                    "subscriber": subscriber
                },
                False
            )
        elif subscriber.type == Subscriber_Module.PHONE:
            status = __deliver_sms(
                subscriber.phone,
                ""
            )
        elif subscriber.type == Subscriber_Module.ENDPOINT:
            status = __deliver_webhook(
                subscriber.endpoint,
                subscriber.auth_token,
                '{}' % ()
            )

        if status:
            # message sent again
            incident_update_notification_module.update_one_by_id(notification["id"], {
                "status": "success"
            })

    return {
        "status": "passed",
        "result": "{}",
        "notify_type": "passed"
    }


def __deliver_email(app_name, app_email, app_url, recipients, subject, template, data={}, fail_silently=False):
    try:
        send_mail(
            subject,
            "",
            app_email,
            recipients,
            fail_silently=fail_silently,
            html_message=render_to_string(template, {
                "app_url": app_url,
                "app_name": app_name,
                "subject": subject
            })
        )
        return True
    except Exception:
        return False


def __deliver_sms(phone_number, message):
    # Not Supported Yet
    return False


def __deliver_webhook(endpoint, auth_token, payload):
    try:
        headers = {
            "X-AUTH-TOKEN": auth_token
        }
        requests.post(endpoint, headers=headers, data=payload)
        return True
    except Exception:
        return False
