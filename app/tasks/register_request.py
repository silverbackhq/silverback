# Copyright 2019 Silverbackhq
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
