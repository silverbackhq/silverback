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

# Standard Library
import json

# Third Party Library
from celery import shared_task
from django.utils.translation import gettext as _

# Local Library
from app.modules.util.helpers import Helpers
from app.modules.core.subscriber import Subscriber as SubscriberModule


@shared_task
def verify_subscriber(subscriber_id, correlation_id=""):
    logger = Helpers().get_logger(__name__)

    logger.info(
        _("Worker started processing verify_subscriber task with parameters %(parameters)s {'correlationId':'%(correlationId)s'}") % {
            "parameters": json.dumps({}),
            "correlationId": correlation_id
        }
    )

    subscriber_module = SubscriberModule()
    subscriber = subscriber_module.get_one_by_id(subscriber_id)

    if not subscriber:
        return {
            "status": "passed",
            "result": "{}"
        }

    if subscriber.type == SubscriberModule.EMAIL:
        result = __verify_email()
    elif subscriber.type == SubscriberModule.PHONE:
        result = __verify_phone()
    elif subscriber.type == SubscriberModule.ENDPOINT:
        result = __verify_endpoint()

    return result


@shared_task
def __verify_email():
    pass


@shared_task
def __verify_phone():
    pass


@shared_task
def __verify_endpoint():
    pass
