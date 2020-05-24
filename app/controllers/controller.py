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
from app.settings.info import AUTHOR
from app.settings.info import COPYRIGHT
from app.settings.info import LICENSE
from app.settings.info import VERSION
from app.settings.info import MAINTAINER
from app.settings.info import EMAIL
from app.settings.info import STATUS
from app.settings.info import REPO_URL
from app.settings.info import AUTHOR_URL
from app.settings.info import RELEASES
from app.settings.info import SUPPORT_URL
from app.modules.util.gravatar import Gravatar
from app.modules.entity.option_entity import OptionEntity
from app.modules.entity.user_entity import UserEntity
from app.modules.util.helpers import Helpers
from app.modules.validation.extension import ExtraRules
from app.exceptions.server_error import ServerError


class Controller():
    """Base Controller"""

    __helpers = None
    __form = None
    __logger = None
    __option_entity = OptionEntity()
    __user_entity = UserEntity()
    __data = {
        "AUTHOR": AUTHOR,
        "COPYRIGHT": COPYRIGHT,
        "LICENSE": LICENSE,
        "VERSION": VERSION,
        "MAINTAINER": MAINTAINER,
        "EMAIL": EMAIL,
        "STATUS": STATUS,
        "REPO_URL": REPO_URL,
        "AUTHOR_URL": AUTHOR_URL,
        "RELEASES": RELEASES,
        "SUPPORT_URL": SUPPORT_URL
    }

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

    def load_options(self, options):
        options_to_load = {}
        for key in options.keys():
            options_to_load[key] = options[key]
            if key not in self.__data.keys():
                self.__data[key] = options[key]

        if len(options_to_load.keys()) > 0:
            new_options = self.__option_entity.get_many_by_keys(options_to_load.keys())
            for option in new_options:
                self.__data[option.key] = option.value

    def autoload_options(self):
        options = self.__option_entity.get_many_by_autoload(True)
        for option in options:
            self.__data[option.key] = option.value

    def autoload_user(self, user_id):
        user_data = {
            "user_first_name": "",
            "user_last_name": "",
            "user_username": "",
            "user_email": "",
            "user_avatar": ""
        }

        if user_id is not None:
            user = self.__user_entity.get_one_by_id(user_id)
            if user is not False:
                user_data["user_first_name"] = user.first_name
                user_data["user_last_name"] = user.last_name
                user_data["user_username"] = user.username
                user_data["user_email"] = user.email
                user_data["user_avatar"] = Gravatar(user.email).get_image()

        self.__data.update(user_data)

    def context_push(self, new_data):
        self.__data.update(new_data)

    def context_get(self, key=None, default=None):
        if key is not None:
            return self.__data[key] if key in self.__data else default
        return self.__data
