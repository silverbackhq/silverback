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
import json

# Third Party Library
from django.views import View
from django.utils.translation import gettext as _

# Local Library
from app.controllers.controller import Controller
from app.modules.core.decorators import stop_request_if_authenticated
from app.modules.core.user import User as UserModule


class Register(View, Controller):
    """Register Private Endpoint Controller"""

    def __init__(self):
        self.__user = UserModule()

    @stop_request_if_authenticated
    def post(self, request):

        self.__correlation_id = self.get_correlation(request)

        self.get_request().set_request(request)

        request_data = self.get_request().get_request_data("post", {
            "register_request_token": "",
            "first_name": "",
            "last_name": "",
            "username": "",
            "email": "",
            "password": ""
        })

        self.get_form().add_inputs({
            'first_name': {
                'value': request_data["first_name"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'sv_names': {
                        'error': _('Error! First name contains invalid characters.')
                    },
                    'length_between': {
                        'param': [0, 20],
                        'error': _('Error! First name must be 1 to 20 characters long.')
                    }
                }
            },
            'last_name': {
                'value': request_data["last_name"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'sv_names': {
                        'error': _('Error! Last name contains invalid characters.')
                    },
                    'length_between': {
                        'param': [0, 20],
                        'error': _('Error! Last name must be 1 to 20 characters long.')
                    }
                }
            },
            'username': {
                'value': request_data["username"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'alpha_numeric': {
                        'error': _('Error! Username must be alpha numeric.')
                    },
                    'length_between': {
                        'param': [4, 10],
                        'error': _('Error! Username must be 5 to 10 characters long.')
                    }
                }
            },
            'email': {
                'value': request_data["email"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'sv_email': {
                        'error': _('Error! Admin email is invalid.')
                    }
                }
            },
            'password': {
                'value': request_data["password"],
                'validate': {
                    'sv_password': {
                        'error': _('Error! Password must contain at least uppercase letter, lowercase letter, numbers and special character.')
                    },
                    'length_between': {
                        'param': [7, 20],
                        'error': _('Error! Password length must be from 8 to 20 characters.')
                    }
                }
            }
        })

        self.get_form().process()

        if not self.get_form().is_passed():
            return self.json(self.get_form().get_errors())

        register_request = self.__user.get_register_request_by_token(request_data["register_request_token"])

        if not register_request:
            return self.json([{
                "type": "error",
                "message": _("Error! Register token is invalid or expired.")
            }])

        payload = json.loads(register_request.payload)

        if self.__user.username_used(self.get_form().get_sinput("username")):
            return self.json([{
                "type": "error",
                "message": _("Error! Username is already used.")
            }])

        if self.__user.email_used(self.get_form().get_sinput("email")):
            return self.json([{
                "type": "error",
                "message": _("Error! Email is already used for other account.")
            }])

        result = self.__user.insert_one({
            "username": self.get_form().get_sinput("username"),
            "email": self.get_form().get_sinput("email"),
            "first_name": self.get_form().get_sinput("first_name"),
            "last_name": self.get_form().get_sinput("last_name"),
            "password": self.get_form().get_sinput("password"),
            "is_staff": False,
            "is_active": True,
            "is_superuser": True if payload["role"] == "admin" else False
        })

        if result:
            self.__user.delete_register_request_by_token(request_data["register_request_token"])
            return self.json([{
                "type": "success",
                "message": _("Account created successfully.")
            }])
        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while creating your account.")
            }])
