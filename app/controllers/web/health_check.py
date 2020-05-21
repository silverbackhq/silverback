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
from django.views import View
from django.http import JsonResponse
from django.utils.translation import gettext as _

# Local Library
from app.modules.core.health import Health
from app.modules.util.helpers import Helpers


class HealthCheck(View):
    """Health Check Page Controller"""

    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__health = Health()
        self.__helpers = Helpers()
        self.__logger = self.__helpers.get_logger(__name__)

        status = Health.OK
        errors = []
        errors.extend(self.__health.check_db())
        errors.extend(self.__health.check_io())
        errors.extend(self.__health.check_workers())

        if len(errors) > 0:
            status = Health.NOT_OK
            self.__logger.error(_("Health Check Result: %(status)s %(errors)s {'correlationId':'%(correlationId)s'}") % {
                "status": status,
                "errors": self.__helpers.json_dumps(errors),
                "correlationId": self.__correlation_id
            })
        else:
            self.__logger.info(_("Health Check Result: %(status)s %(errors)s {'correlationId':'%(correlationId)s'}") % {
                "status": status,
                "errors": self.__helpers.json_dumps(errors),
                "correlationId": self.__correlation_id
            })

        return JsonResponse({
            "status": status,
            "messages": []
        }, status=200 if status == Health.OK else 503)
