"""
    Register Request Tasks
    ~~~~~~~~~~~~~~

    :copyright: silverbackhq
    :license: BSD-3-Clause
"""

# Third Party Library
from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string


@shared_task
def register_request_email(app_name, app_email, app_url, recipient_list, token, subject, template, fail_silently=False):
    try:
        send_mail(
            subject,
            "",
            app_email,
            recipient_list,
            fail_silently=fail_silently,
            html_message=render_to_string(template, {
                "app_url": app_url,
                "token": token,
                "app_name": app_name,
                "subject": subject
            }))
        return {
            "status": "passed",
            "result": "{}"
        }
    except Exception as e:
        return {
            "status": "failed",
            "result": {
                "error": str(e)
            }
        }
