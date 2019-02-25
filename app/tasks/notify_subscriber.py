"""
Notify Subscriber Tasks
"""

# Django
import os
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext as _
from django.urls import reverse

# Third party
import messagebird
import requests
import markdown2
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

    data = {}
    data["incident_uri"] = incident.uri
    data["incident_update_time"] = incident_update.datetime.strftime("%b %d %Y %H:%M:%S")
    data["incident_type"] = incident_update.status.title()
    data["incident_update"] = markdown2.markdown(incident_update.message)

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
                data,
                False
            )
        elif subscriber.type == Subscriber_Module.PHONE:
            status = __deliver_sms(
                app_name,
                subscriber.phone,
                reverse("app.web.incidents", kwargs={'uri': incident.uri})
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
                data,
                False
            )
        elif subscriber.type == Subscriber_Module.PHONE:
            status = __deliver_sms(
                app_name,
                subscriber.phone,
                reverse("app.web.incidents", kwargs={'uri': incident.uri})
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
                "subject": subject,
                "incident_type": data["incident_type"],
                "incident_update": data["incident_update"],
                "incident_update_time": data["incident_update_time"],
                "incident_uri": data["incident_uri"]
            })
        )
        return True
    except Exception:
        return False


def __deliver_sms(app_name, phone_number, message):
    if os.getenv("TEXT_MESSAGING_DRIVER", "messagebird") == "messagebird":
        try:
            client = messagebird.Client(os.getenv("MESSAGEBIRD_API_KEY", ""))
            msg = client.message_create(app_name, phone_number, message, {})
            return True if msg.id else False
        except Exception:
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
