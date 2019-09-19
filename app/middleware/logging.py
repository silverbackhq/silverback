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
from django.utils.translation import gettext as _

# Local Library
from app.modules.util.helpers import Helpers


class Logging():

    def __init__(self, get_response):
        self.__helpers = Helpers()
        self.get_response = get_response
        self.__logger = self.__helpers.get_logger(__name__)

    def __call__(self, request):
        correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""

        self.__logger.debug(_("Request Method: %(method)s {'correlationId':'%(correlationId)s'}") % {
            "method": request.method,
            "correlationId": correlation_id
        })
        self.__logger.debug(_("Request URL: %(path)s {'correlationId':'%(correlationId)s'}") % {
            "path": request.path,
            "correlationId": correlation_id
        })
        self.__logger.debug(_("Request Body: %(body)s {'correlationId':'%(correlationId)s'}") % {
            "body": self.__hide_secure_values(request.body),
            "correlationId": correlation_id
        })

        response = self.get_response(request)

        return response

    def __hide_secure_values(self, request_body):
        filtered_body = []
        request_body = str(request_body)
        if len(request_body) == 0:
            return "&".join(filtered_body)

        if "&" in request_body:
            request_body = request_body.split("&")
            for item in request_body:
                if "=" in item:
                    item = item.split("=")
                    if "password" in item[0]:
                        item[1] = "<hidden>"
                    if "token" in item[0]:
                        item[1] = "<hidden>"
                    filtered_body.append("%s=%s" % (item[0], item[1]))

        return "&".join(filtered_body)
