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


@shared_task
def ping(text="PONG", correlation_id=""):
    logger = Helpers().get_logger(__name__)

    logger.info(_("Worker started processing ping task with parameters %(parameters)s {'correlationId':'%(correlationId)s'}") % {
        "parameters": json.dumps({"text": text}),
        "correlationId": correlation_id
    })

    return {"status": "passed", "result": text}
