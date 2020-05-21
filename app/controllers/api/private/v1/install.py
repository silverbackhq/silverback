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
from django.http import JsonResponse
from django.utils.translation import gettext as _

# Local Library
from pyvalitron.form import Form
from app.modules.util.helpers import Helpers
from app.modules.core.request import Request
from app.modules.core.response import Response
from app.modules.validation.extension import ExtraRules
from app.modules.core.install import Install as InstallModule
from app.modules.core.decorators import stop_request_if_installed
from app.modules.core.notification import Notification as NotificationModule


class Install(View):
    """Install Private Endpoint Controller"""

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__install = InstallModule()
        self.__notification = NotificationModule()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__correlation_id = ""
        self.__form.add_validator(ExtraRules())

    @stop_request_if_installed
    def post(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""

        self.__logger.info(_("Check if application is installed"))

        if self.__install.is_installed():
            self.__logger.error(_("Application is already installed"))

            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Application is already installed.")
            }], {}, self.__correlation_id))

        self.__logger.info(_("Validate incoming request data"))

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
                    'strip': {}
                },
                'validate': {
                    'alpha_numeric': {
                        'error': _('Error! Application name must be alpha numeric.')
                    },
                    'length_between': {
                        'param': [2, 30],
                        'error': _('Error! Application name must be 2 to 30 characters long.')
                    }
                }
            },
            'app_email': {
                'value': request_data["app_email"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'sv_email': {
                        'error': _('Error! Application email is invalid.')
                    }
                }
            },
            'app_url': {
                'value': request_data["app_url"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'sv_url': {
                        'error': _('Error! Application url is invalid.')
                    }
                }
            },
            'admin_username': {
                'value': request_data["admin_username"],
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
            'admin_email': {
                'value': request_data["admin_email"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'sv_email': {
                        'error': _('Error! Admin email is invalid.')
                    }
                }
            },
            'admin_password': {
                'value': request_data["admin_password"],
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

        self.__form.process()

        if not self.__form.is_passed():
            self.__logger.info(_("Request data is invalid"))
            return JsonResponse(self.__response.send_errors_failure(self.__form.get_errors(), {}, self.__correlation_id))

        self.__install.set_app_data(
            self.__form.get_sinput("app_name"),
            self.__form.get_sinput("app_email"),
            self.__form.get_sinput("app_url")
        )
        self.__install.set_admin_data(
            self.__form.get_sinput("admin_username"),
            self.__form.get_sinput("admin_email"),
            self.__form.get_sinput("admin_password")
        )

        try:
            self.__logger.info(_("Run database migrations, store options and create admin account"))
            user_id = self.__install.install()
        except Exception as exception:
            self.__logger.error(_("Something went wrong during installation"))
            self.__logger.error(_("Internal server error during installation: %(exception)s {'correlationId':'%(correlationId)s'}") % {
                "exception": exception,
                "correlationId": self.__correlation_id
            })

        if user_id:
            self.__logger.info(_("Application installed successfully. Trigger a notification"))
            self.__notification.create_notification({
                "highlight": _('Installation'),
                "notification": _('Silverback installed successfully'),
                "url": "#",
                "type": NotificationModule.MESSAGE,
                "delivered": False,
                "user_id": user_id,
                "task_id": None
            })

            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Application installed successfully.")
            }], {}, self.__correlation_id))
        else:
            self.__logger.error(_("Something went wrong during installation"))
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something went wrong during installation.")
            }], {}, self.__correlation_id))
