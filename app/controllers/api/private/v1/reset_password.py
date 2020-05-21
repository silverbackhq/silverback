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
from app.modules.core.reset_password import ResetPassword as ResetPasswordModule


class ResetPassword(View, Controller):
    """Reset Password Private Endpoint Controller"""

    def __init__(self):
        self.__reset_password = ResetPasswordModule()

    @stop_request_if_authenticated
    def post(self, request):

        self.__correlation_id = self.get_correlation(request)

        self.get_request().set_request(request)

        request_data = self.get_request().get_request_data("post", {
            "reset_token": "",
            "new_password": ""
        })

        self.get_form().add_inputs({
            'reset_token': {
                'value': request_data["reset_token"],
                'sanitize': {
                    'escape': {},
                    'strip': {}
                },
                'validate': {}
            },
            'new_password': {
                'value': request_data["new_password"],
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

        if not self.__reset_password.check_token(self.get_form().get_sinput("reset_token")):
            return self.json([{
                "type": "error",
                "message": _("Error! Reset token is expired or invalid.")
            }])

        result = self.__reset_password.reset_password(
            self.get_form().get_sinput("reset_token"),
            self.get_form().get_sinput("new_password")
        )

        result &= self.__reset_password.delete_reset_request(self.get_form().get_sinput("reset_token"))

        if not result:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while resetting password.")
            }])
        else:
            return self.json([{
                "type": "success",
                "message": _("Password updated successfully.")
            }])
