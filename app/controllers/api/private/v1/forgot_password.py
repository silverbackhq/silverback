"""
Forgot Password API Endpoint
"""

# Django
from django.views import View
from django.http import JsonResponse
from django.utils.translation import gettext as _

# local Django
from pyvalitron.form import Form
from app.modules.validation.extension import ExtraRules
from app.modules.util.helpers import Helpers
from app.modules.core.request import Request
from app.modules.core.response import Response
from app.modules.core.decorators import stop_request_if_authenticated
from app.modules.core.forgot_password import Forgot_Password as Forgot_Password_Module


class Forgot_Password(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __forgot_password = None
    __logger = None
    __correlation_id = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__forgot_password = Forgot_Password_Module()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__form.add_validator(ExtraRules())

    @stop_request_if_authenticated
    def post(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"]
        self.__request.set_request(request)

        request_data = self.__request.get_request_data("post", {
            "email": ""
        })

        self.__form.add_inputs({
            'email': {
                'value': request_data["email"],
                'sanitize': {
                    'escape': {},
                    'strip': {}
                },
                'validate': {
                    'sv_email': {
                        'error': _('Error! Email is invalid.')
                    }
                }
            }
        })

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_errors_failure(self.__form.get_errors()))

        if not self.__forgot_password.check_email(self.__form.get_sinput("email")):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Email is not exist.")
            }]))

        reset_request = self.__forgot_password.reset_request_exists(self.__form.get_sinput("email"))

        if reset_request:
            if self.__forgot_password.is_spam(reset_request):
                return JsonResponse(self.__response.send_private_failure([{
                    "type": "error",
                    "message": _("Sorry! You already exceeded the maximum number of reset requests!")
                }]))
            token = self.__forgot_password.update_request(reset_request)
        else:
            token = self.__forgot_password.create_request(self.__form.get_sinput("email"))

        if not token:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while creating reset request.")
            }]))

        message = self.__forgot_password.send_message(self.__form.get_sinput("email"), token)

        if not message:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while sending reset instructions.")
            }]))
        else:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Reset instructions sent successfully.")
            }]))
