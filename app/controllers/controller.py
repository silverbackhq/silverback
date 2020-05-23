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
from http import HTTPStatus

# Third Party Library
from django.http import JsonResponse
from django.utils.translation import gettext as _
from pyvalitron.form import Form

# Local Library
from app.modules.util.helpers import Helpers
from app.modules.validation.extension import ExtraRules
from app.exceptions.server_error import ServerError


class Controller():
    """Base Controller"""

    __helpers = None
    __form = None
    __logger = None

    def json(self, messages, payload={}, status="success", status_code=HTTPStatus.OK):
        response = {
            "status": status
        }

        # if validation messages
        if isinstance(messages, dict):
            errors = []
            for input_key, error_list in messages.items():
                for error in error_list:
                    errors.append({"type": "error", "message": error})
            messages = errors

        if not isinstance(messages, list):
            raise ServerError(_("Invalid messages type %s passed to controller.json") % (type(messages)))

        response["messages"] = messages

        # Change status to failure if one message has type error
        for message in messages:
            if message["type"] == "error":
                response["status"] = "failure"

        if len(payload) > 0:
            response["payload"] = payload

        return JsonResponse(response, status=status_code)

    def correlation(self, request):
        return request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""

    def logger(self, request):
        if not self.__logger:
            self.__helpers = self.helpers()
            self.__logger = self.__helpers.get_logger(__name__)

        return self.__logger

    def get_request_data(self, request, method, predicted):
        request_data = {}
        log_data = {}
        data_bag = request.POST if method.lower() == "post" else request.GET

        for key, default in predicted.items():
            if "password" in key:
                log_data[key] = "<hidden>" if key in data_bag else default
            elif "token" in key:
                log_data[key] = "<hidden>" if key in data_bag else default
            else:
                log_data[key] = data_bag[key] if key in data_bag else default
            request_data[key] = data_bag[key] if key in data_bag else default

        self.logger(request).info(_("Required request data: %(data)s") % {
            "data": self.helpers().json_dumps(log_data)
        })

        return request_data

    def helpers(self):
        if not self.__helpers:
            self.__helpers = Helpers()
        return self.__helpers

    def form(self):
        if not self.__form:
            self.__form = Form()
            self.__form.add_validator(ExtraRules())
        return self.__form
