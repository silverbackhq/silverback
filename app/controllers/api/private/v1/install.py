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
from app.modules.core.install import Install as InstallModule
from app.modules.core.decorators import stop_request_if_installed
from app.modules.core.notification import Notification as NotificationModule


class Install(View, Controller):
    """Install Private Endpoint Controller"""

    def __init__(self):
        self.__install = InstallModule()
        self.__notification = NotificationModule()

    @stop_request_if_installed
    def post(self, request):

        if self.__install.is_installed():
            return self.json([{
                "type": "error",
                "message": _("Error! Application is already installed.")
            }])

        request_data = self.get_request_data(request, "post", {
            "app_name": "",
            "app_email": "",
            "app_url": "",
            "admin_username": "",
            "admin_email": "",
            "admin_password": ""
        })

        self.form().add_inputs({
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

        self.form().process()

        if not self.form().is_passed():
            return self.json(self.form().get_errors())

        self.__install.set_app_data(
            self.form().get_sinput("app_name"),
            self.form().get_sinput("app_email"),
            self.form().get_sinput("app_url")
        )
        self.__install.set_admin_data(
            self.form().get_sinput("admin_username"),
            self.form().get_sinput("admin_email"),
            self.form().get_sinput("admin_password")
        )

        try:
            user_id = self.__install.install()
        except Exception as exception:
            self.logger().error(_("Internal server error during installation: %(exception)s") % {
                "exception": exception
            })

        if user_id:
            self.__notification.create_notification({
                "highlight": _('Installation'),
                "notification": _('Silverback installed successfully'),
                "url": "#",
                "type": NotificationModule.MESSAGE,
                "delivered": False,
                "user_id": user_id,
                "task_id": None
            })

            return self.json([{
                "type": "success",
                "message": _("Application installed successfully.")
            }])
        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something went wrong during installation.")
            }])
