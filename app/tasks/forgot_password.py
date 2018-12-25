"""
Forgot Password Tasks
"""

# Django
from django.core.mail import send_mail
from django.template.loader import render_to_string

# Third party
from celery import shared_task


@shared_task
def forgot_password_email(app_name, app_email, app_url, recipient_list, token, subject, template, fail_silently=False):
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
                "app_name": app_name
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
