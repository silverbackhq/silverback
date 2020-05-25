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
from app.modules.core.decorators import stop_request_if_authenticated
from app.modules.core.forgot_password import ForgotPassword as ForgotPasswordModule


class ForgotPassword(View, Controller):
    """Forgot Password Private Endpoint Controller"""

    def __init__(self):
        self.__forgot_password = ForgotPasswordModule()

    @stop_request_if_authenticated
    def post(self, request):

        request_data = self.get_request_data(request, "post", {
            "email": ""
        })

        self.form().add_inputs({
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

        self.form().process()

        if not self.form().is_passed():
            return self.json(self.form().get_errors())

        if not self.__forgot_password.check_email(self.form().get_sinput("email")):
            return self.json([{
                "type": "error",
                "message": _("Error! Email is not exist.")
            }])

        reset_request = self.__forgot_password.reset_request_exists(self.form().get_sinput("email"))

        if reset_request:
            if self.__forgot_password.is_spam(reset_request):
                return self.json([{
                    "type": "error",
                    "message": _("Sorry! You already exceeded the maximum number of reset requests!")
                }])
            token = self.__forgot_password.update_request(reset_request)
        else:
            token = self.__forgot_password.create_request(self.form().get_sinput("email"))

        if not token:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while creating reset request.")
            }])

        message = self.__forgot_password.send_message(self.form().get_sinput("email"), token)

        if not message:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while sending reset instructions.")
            }])
        else:
            return self.json([{
                "type": "success",
                "message": _("Reset instructions sent successfully.")
            }])
