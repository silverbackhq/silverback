"""
Install API Endpoint
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
from app.modules.core.decorators import stop_request_if_installed
from app.modules.core.install import Install as Install_Module


class Install(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __install = None
    __logger = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__install = Install_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    @stop_request_if_installed
    def post(self, request):

        if self.__install.is_installed():
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Application is already installed.")
            }]))

        self.__request.set_request(request)

        request_data = self.__request.get_request_data("post", {
            "app_name": "",
            "app_email": "",
            "app_url": "",
            "admin_username": "",
            "admin_email": "",
            "admin_password": ""
        })

        self.__form.add_inputs({
            'app_name': {
                'value': request_data["app_name"],
                'sanitize': {
                    'escape': {},
                    'strip': {}
                },
                'validate': {
                    'alpha_numeric': {
                        'error': _('Error! Application name must be alpha numeric.')
                    },
                    'length_between': {
                        'param': [3, 10],
                        'error': _('Error! Application name must be 5 to 10 characters long.')
                    }
                }
            },
            'app_email': {
                'value': request_data["app_email"],
                'sanitize': {
                    'escape': {},
                    'strip': {}
                },
                'validate': {
                    'email': {
                        'error': _('Error! Application email is invalid.')
                    }
                }
            },
            'app_url': {
                'value': request_data["app_url"],
                'sanitize': {
                    'escape': {},
                    'strip': {}
                },
                'validate': {
                    'url': {
                        'error': _('Error! Application url is invalid.')
                    }
                }
            },
            'admin_username': {
                'value': request_data["admin_username"],
                'sanitize': {
                    'escape': {},
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
            'admin_email': {
                'value': request_data["admin_email"],
                'sanitize': {
                    'escape': {},
                    'strip': {}
                },
                'validate': {
                    'email': {
                        'error': _('Error! Admin email is invalid.')
                    }
                }
            },
            'admin_password': {
                'value': request_data["admin_password"],
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

        self.__install.set_app_data(
            self.__form.get_input_value("app_name"),
            self.__form.get_input_value("app_email"),
            self.__form.get_input_value("app_url")
        )
        self.__install.set_admin_data(
            self.__form.get_input_value("admin_username"),
            self.__form.get_input_value("admin_email"),
            self.__form.get_input_value("admin_password")
        )

        if self.__install.install():
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Application installed successfully.")
            }]))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong during installing.")
            }]))
