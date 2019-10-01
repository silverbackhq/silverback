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


class Request():

    def __init__(self, request=None):
        self.__request = request
        self.__helpers = Helpers()
        self.__logger = self.__helpers.get_logger(__name__)

    def set_request(self, request):
        self.__request = request

    def get_request_data(self, method, predicted):
        request_data = {}
        log_data = {}
        correlation_id = self.__request.META["X-Correlation-ID"] if "X-Correlation-ID" in self.__request.META else ""
        data_bag = self.__request.POST if method.lower() == "post" else self.__request.GET

        for key, default in predicted.items():
            if "password" in key:
                log_data[key] = "<hidden>" if key in data_bag else default
            elif "token" in key:
                log_data[key] = "<hidden>" if key in data_bag else default
            else:
                log_data[key] = data_bag[key] if key in data_bag else default
            request_data[key] = data_bag[key] if key in data_bag else default

        self.__logger.debug(_("App Incoming Request: %(data)s {'correlationId':'%(correlationId)s'}") % {
            "data": self.__helpers.json_dumps(log_data),
            "correlationId": correlation_id
        })

        return request_data
