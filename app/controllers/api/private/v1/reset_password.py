"""
Forgot Password API Endpoint
"""

# Django
from django.views import View
from django.http import JsonResponse
from django.utils.translation import gettext as _

# local Django
from app.modules.validation.form import Form
from app.modules.util.helpers import Helpers
from app.modules.core.request import Request
from app.modules.core.response import Response
from app.modules.core.decorators import stop_request_if_authenticated
from app.modules.core.reset_password import Reset_Password as Reset_Password_Module


class Reset_Password(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __reset_password = None
    __logger = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__reset_password = Reset_Password_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    @stop_request_if_authenticated
    def post(self, request):

        self.__request.set_request(request)

        request_data = self.__request.get_request_data("post", {
            "reset_token": "",
            "new_password": ""
        })

        self.__form.add_inputs({
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
                    'password': {
                        'error': _('Error! Password must contain at least uppercase letter, lowercase letter, numbers and special character.')
                    },
                    'length_between': {
                        'param': [7, 20],
                        'error': _('Error! Password length must be from 8 to 20 characters.')
                    }
                }
            }
        })

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_private_failure(self.__form.get_errors(with_type=True)))

        if not self.__reset_password.check_token(self.__form.get_input_value("reset_token")):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Reset token is expired or invalid.")
            }]))

        result = self.__reset_password.reset_password(
            self.__form.get_input_value("reset_token"),
            self.__form.get_input_value("new_password")
        )

        result &= self.__reset_password.delete_reset_request(self.__form.get_input_value("reset_token"))

        if not result:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while resetting password.")
            }]))
        else:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Password updated successfully.")
            }]))
