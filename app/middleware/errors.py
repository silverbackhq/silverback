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
from django.http import JsonResponse
from django.utils.translation import gettext as _

# Local Library
from app.modules.util.helpers import Helpers
from app.exceptions.server_error import ServerError
from app.exceptions.client_error import ClientError

class Errors():

    def __init__(self, get_response):
        self.__helpers = Helpers()
        self.get_response = get_response
        self.__logger = self.__helpers.get_logger(__name__)

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):

        correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""

        if isinstance(exception, ClientError):
            self.__logger.info(
                _("Client error thrown %(method)s:%(path)s  - %(name)s - %(exception)s {'correlationId':'%(correlationId)s'}") % {
                    "method": request.method,
                    "path": request.path,
                    "name": exception.__class__.__name__,
                    "exception": exception,
                    "correlationId": correlation_id
                }
            )
        else:
            self.__logger.error(
                _("The server encountered something unexpected! %(method)s:%(path)s  - %(name)s - %(exception)s {'correlationId':'%(correlationId)s'}") % {
                    "method": request.method,
                    "path": request.path,
                    "name": exception.__class__.__name__,
                    "exception": exception,
                    "correlationId": correlation_id
                }
            )

            self.__logger.exception(exception)

        if request.is_ajax():
            return JsonResponse({
                "status": "failure",
                "messages": [{
                    "type": "error",
                    "message": str(exception) if isinstance(exception, ClientError)
                        else _("Something goes wrong! Please contact a system administrator.")
                }]
            })

        return None
