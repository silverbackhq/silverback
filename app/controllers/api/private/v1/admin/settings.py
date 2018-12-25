"""
Settings API Endpoint
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
from app.modules.core.settings import Settings as Settings_Module
from app.modules.core.acl import ACL


class Settings(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __settings_module = None
    __logger = None
    __acl = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__settings_module = Settings_Module()
        self.__acl = ACL()
        self.__logger = self.__helpers.get_logger(__name__)

    def post(self, request):

        if not self.__acl.user_has_permission(request.user.id, "manage_settings"):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Invalid Request.")
            }]))

        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
            "app_name": "",
            "app_email": "",
            "app_url": "",
            "app_description": "",
            "google_analytics_account": "",
            "reset_mails_messages_count": "",
            "reset_mails_expire_after": "",
            "access_tokens_expire_after": "",
            "prometheus_token": ""
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
            'app_description': {
                'value': request_data["app_description"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [0, 300],
                        'error': _('Error! App description is very long.')
                    },
                    'optional': {}
                }
            },
            "prometheus_token": {
                'value': request_data["prometheus_token"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [0, 100],
                        'error': _('Error! Prometheus token is invalid.')
                    },
                    'optional': {}
                }
            },
            'google_analytics_account': {
                'value': request_data["google_analytics_account"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [0, 30],
                        'error': _('Error! Google analytics account is invalid.')
                    },
                    'optional': {}
                }
            },
            'reset_mails_messages_count': {
                'value': request_data["reset_mails_messages_count"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'digit': {
                        'error': _('Error! Reset mails count is invalid.')
                    },
                    'greater_than': {
                        'error': _('Error! Reset mails count is invalid.'),
                        'param': [0]
                    }
                }
            },
            'reset_mails_expire_after': {
                'value': request_data["reset_mails_expire_after"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'digit': {
                        'error': _('Error! Reset mails expiry interval is invalid.')
                    },
                    'greater_than': {
                        'error': _('Error! Reset mails count is invalid.'),
                        'param': [0]
                    }
                }
            },
            'access_tokens_expire_after': {
                'value': request_data["access_tokens_expire_after"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'digit': {
                        'error': _('Error! Access token expiry interval is invalid.')
                    },
                    'greater_than': {
                        'error': _('Error! Access token expiry interval is invalid.'),
                        'param': [0]
                    }
                }
            },
        })

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_private_failure(self.__form.get_errors(with_type=True)))

        result = self.__settings_module.update_options({
            "app_name": self.__form.get_input_value("app_name"),
            "app_email": self.__form.get_input_value("app_email"),
            "app_url": self.__form.get_input_value("app_url"),
            "app_description": self.__form.get_input_value("app_description"),
            "google_analytics_account": self.__form.get_input_value("google_analytics_account"),
            "reset_mails_messages_count": self.__form.get_input_value("reset_mails_messages_count"),
            "reset_mails_expire_after": self.__form.get_input_value("reset_mails_expire_after"),
            "access_tokens_expire_after": self.__form.get_input_value("access_tokens_expire_after"),
            "prometheus_token": self.__form.get_input_value("prometheus_token")
        })

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Settings updated successfully.")
            }]))

        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating settings.")
            }]))
