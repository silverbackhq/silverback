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
from pyvalitron.form import Form
from django.http import JsonResponse
from django.utils.translation import gettext as _

# Local Library
from app.modules.util.helpers import Helpers
from app.modules.core.request import Request
from app.modules.core.response import Response
from app.modules.validation.extension import ExtraRules
from app.modules.core.subscriber import Subscriber as SubscriberModule


class StatusSubscribe(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __subscriber = None
    __correlation_id = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__subscriber = SubscriberModule()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__form.add_validator(ExtraRules())

    def post(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""

        self.__request.set_request(request)

        request_data = self.__request.get_request_data("post", {
            "type": "",
            "email": "",
            "phone": "",
            "endpoint": "",
            "auth_token": ""
        })

        if request_data["type"] == "email":

            self.__form.add_inputs({
                'email': {
                    'value': request_data["email"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'sv_email': {
                            'error': _('Error! Email is invalid.')
                        }
                    }
                }
            })

        elif request_data["type"] == "phone":

            self.__form.add_inputs({
                'phone': {
                    'value': request_data["phone"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'sv_phone': {
                            'error': _('Error! Phone number is invalid.')
                        }
                    }
                }
            })

        elif request_data["type"] == "endpoint":

            self.__form.add_inputs({
                'email': {
                    'value': request_data["email"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'sv_email': {
                            'error': _('Error! Email is invalid.')
                        }
                    }
                },
                'endpoint': {
                    'value': request_data["endpoint"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'sv_url': {
                            'error': _('Error! Endpoint URL is invalid.')
                        }
                    }
                },
                'auth_token': {
                    'value': request_data["auth_token"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'length_between': {
                            'param': [0, 80],
                            'error': _('Error! Token is very long.')
                        },
                        'optional': {}
                    }
                }
            })

        else:

            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Invalid request.")
            }], {}, self.__correlation_id))

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_errors_failure(self.__form.get_errors(), {}, self.__correlation_id))

        external_id = self.__helpers.generate_uuid()

        while self.__subscriber.get_one_by_external_id(external_id) is not False:
            external_id = self.__helpers.generate_uuid()

        if request_data["type"] == "email":
            result = self.__subscriber.insert_one({
                "status": "pending",
                "type": "email",
                "email": self.__form.get_sinput("email"),
                "phone": "",
                "endpoint": "",
                "auth_token": "",
                "external_id": external_id
            })

        elif request_data["type"] == "phone":
            result = self.__subscriber.insert_one({
                "status": "pending",
                "type": "phone",
                "email": "",
                "phone": self.__form.get_sinput("phone"),
                "endpoint": "",
                "auth_token": "",
                "external_id": external_id
            })

        else:
            result = self.__subscriber.insert_one({
                "status": "pending",
                "type": "endpoint",
                "email": self.__form.get_sinput("email"),
                "phone": "",
                "endpoint": self.__form.get_sinput("endpoint"),
                "auth_token": self.__form.get_sinput("auth_token"),
                "external_id": external_id
            })

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("You have successfully subscribed.")
            }], {}, self.__correlation_id))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while subscribing.")
            }], {}, self.__correlation_id))
