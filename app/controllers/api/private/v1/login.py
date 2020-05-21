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
from app.modules.core.login import Login as LoginModule
from app.modules.core.decorators import stop_request_if_authenticated
from app.controllers.controller import Controller


class Login(View, Controller):
    """Login Private Endpoint Controller"""

    def __init__(self):
        super(Login, self).__init__()
        self.__login = LoginModule()

    @stop_request_if_authenticated
    def post(self, request):

        self.__correlation_id = self.get_correlation(request);

        if self.__login.is_authenticated(request):
            return self.json([{
                "type": "error",
                "message": _("Error! User is already authenticated.")
            }], "success")

        self.get_request().set_request(request)

        request_data = self.get_request().get_request_data("post", {
            "username": "",
            "password": ""
        })

        self.get_form().add_inputs({
            'username': {
                'value': request_data["username"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'sv_username_or_email': {
                        'error': _("Error! Username or password is invalid.")
                    }
                }
            },
            'password': {
                'value': request_data["password"],
                'validate': {
                    'sv_password': {
                        'error': _("Error! Username or password is invalid.")
                    },
                    'length_between': {
                        'param': [7, 20],
                        'error': _("Error! Username or password is invalid.")
                    }
                }
            }
        })

        self.get_form().process()

        if not self.get_form().is_passed():
            return self.json(self.get_form().get_errors(), "failure")

        if self.__login.authenticate(self.get_form().get_sinput("username"), self.get_form().get_sinput("password"), request):
            return self.json([{
                "type": "success",
                "message": _("You logged in successfully.")
            }], "success")

        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Username or password is invalid.")
            }], "failure")
