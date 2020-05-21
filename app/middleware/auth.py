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
from app.middleware.correlation import CorrelationFilter


class Auth():

    def __init__(self, get_response):
        self.__helpers = Helpers()
        self.get_response = get_response
        self.__roles = {}
        self.__logger = self.__helpers.get_logger(__name__)

    def __call__(self, request):
        correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""

        self.__logger.addFilter(CorrelationFilter(correlation_id))

        self.__logger.info(_("Authorize %(method)s Request to %(path)s") % {
            "method": request.method,
            "path": request.path
        })

        response = self.get_response(request)

        return response
