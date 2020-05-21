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
from django.utils.translation import gettext as _

# Local Library
from app.controllers.controller import Controller
from app.modules.core.subscriber import Subscriber as SubscriberModule


class StatusSubscribe(View, Controller):
    """Subscribe Private Endpoint Controller"""

    def __init__(self):
        self.__subscriber = SubscriberModule()

    def post(self, request):

        self.__correlation_id = self.get_correlation(request)

        self.get_request().set_request(request)

        request_data = self.get_request().get_request_data("post", {
            "type": "",
            "email": "",
            "phone": "",
            "endpoint": "",
            "auth_token": ""
        })

        if request_data["type"] == "email":

            self.get_form().add_inputs({
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

            self.get_form().add_inputs({
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

            self.get_form().add_inputs({
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

            return self.json([{
                "type": "error",
                "message": _("Error! Invalid request.")
            }])

        self.get_form().process()

        if not self.get_form().is_passed():
            return self.json(self.get_form().get_errors())

        external_id = self.get_helpers().generate_uuid()

        while self.__subscriber.get_one_by_external_id(external_id) is not False:
            external_id = self.get_helpers().generate_uuid()

        if request_data["type"] == "email":
            result = self.__subscriber.insert_one({
                "status": "pending",
                "type": "email",
                "email": self.get_form().get_sinput("email"),
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
                "phone": self.get_form().get_sinput("phone"),
                "endpoint": "",
                "auth_token": "",
                "external_id": external_id
            })

        else:
            result = self.__subscriber.insert_one({
                "status": "pending",
                "type": "endpoint",
                "email": self.get_form().get_sinput("email"),
                "phone": "",
                "endpoint": self.get_form().get_sinput("endpoint"),
                "auth_token": self.get_form().get_sinput("auth_token"),
                "external_id": external_id
            })

        if result:
            return self.json([{
                "type": "success",
                "message": _("You have successfully subscribed.")
            }])
        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while subscribing.")
            }])
