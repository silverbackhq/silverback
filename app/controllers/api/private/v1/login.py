"""
Login API Endpoint
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
from app.modules.core.login import Login as Login_Module
from app.modules.core.decorators import stop_request_if_authenticated


class Login(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __login = None
    __logger = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__login = Login_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    @stop_request_if_authenticated
    def post(self, request):
        if self.__login.is_authenticated(request):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! User is already authenticated.")
            }]))

        self.__request.set_request(request)

        request_data = self.__request.get_request_data("post", {
            "username": "",
            "password": ""
        })

        self.__form.add_inputs({
            'username': {
                'value': request_data["username"],
                'sanitize': {
                    'escape': {},
                    'strip': {}
                },
                'validate': {
                    'username_or_email': {
                        'error': _("Error! Username or password is invalid.")
                    }
                }
            },
            'password': {
                'value': request_data["password"],
                'validate': {
                    'password': {
                        'error': _("Error! Username or password is invalid.")
                    },
                    'length_between': {
                        'param': [7, 20],
                        'error': _("Error! Username or password is invalid.")
                    }
                }
            }
        })

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_private_failure(self.__form.get_errors(with_type=True)))

        if self.__login.authenticate(self.__form.get_input_value("username"), self.__form.get_input_value("password"), request):
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("You logged in successfully.")
            }]))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Username or password is invalid.")
            }]))
