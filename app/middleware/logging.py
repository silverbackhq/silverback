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

import json

# Third Party Library
from django.utils.translation import gettext as _

# Local Library
from app.modules.util.helpers import Helpers

# Third Party
from django.http import JsonResponse


class Logging():

    def __init__(self, get_response):
        self.__helpers = Helpers()
        self.get_response = get_response
        self.__logger = self.__helpers.get_logger(__name__)

    def __call__(self, request):

        self.__logger.info(_("Incoming %(method)s Request to %(path)s with %(body)s") % {
            "method": request.method,
            "path": request.path,
            "body": self.__hide_secure_values_from_request(request.body)
        })

        response = self.get_response(request)

        if isinstance(response, JsonResponse):
            self.__logger.info(_("Outgoing %(status)s Response to %(path)s with %(body)s") % {
                "status": response.status_code,
                "path": request.path,
                "body": self.__hide_secure_values_from_response(json.loads(response.content))
            })
        else:
            self.__logger.info(_("Outgoing %(status)s Response to %(path)s: <html>..") % {
                "status": response.status_code,
                "path": request.path
            })

        return response

    def __hide_secure_values_from_response(self, response):
        if "payload" in response:
            for key, value in response["payload"].items():
                if "password" in key:
                    response["payload"][key] = "<hidden>"
                elif "token" in key:
                    response["payload"][key] = "<hidden>"
                else:
                    response["payload"][key] = value
        return response

    def __hide_secure_values_from_request(self, request_body):
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
