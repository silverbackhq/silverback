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
from app.modules.core.acl import ACL
from app.controllers.controller import Controller
from app.modules.core.settings import Settings as SettingsModule
from app.modules.core.activity import Activity as ActivityModule
from app.modules.core.decorators import allow_if_authenticated_and_has_permission


class Settings(View, Controller):
    """Update Settings Private Endpoint Controller"""

    def __init__(self):
        self.__settings_module = SettingsModule()
        self.__acl = ACL()
        self.__activity_module = ActivityModule()

    @allow_if_authenticated_and_has_permission("manage_settings")
    def post(self, request):

        self.__correlation_id = self.get_correlation(request)
        self.get_request().set_request(request)
        request_data = self.get_request().get_request_data("post", {
            "app_name": "",
            "app_email": "",
            "app_url": "",
            "app_description": "",
            "google_analytics_account": "",
            "reset_mails_messages_count": "",
            "reset_mails_expire_after": "",
            "access_tokens_expire_after": "",
            "prometheus_token": "",
            "newrelic_api_key": ""
        })

        self.get_form().add_inputs({
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
            "newrelic_api_key": {
                'value': request_data["newrelic_api_key"],
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
                'value': int(request_data["reset_mails_messages_count"]),
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'greater_than': {
                        'error': _('Error! Reset mails count is invalid.'),
                        'param': [0]
                    }
                }
            },
            'reset_mails_expire_after': {
                'value': int(request_data["reset_mails_expire_after"]),
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'greater_than': {
                        'error': _('Error! Reset mails count is invalid.'),
                        'param': [0]
                    }
                }
            },
            'access_tokens_expire_after': {
                'value': int(request_data["access_tokens_expire_after"]),
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'greater_than': {
                        'error': _('Error! Access token expiry interval is invalid.'),
                        'param': [0]
                    }
                }
            },
        })

        self.get_form().process()

        if not self.get_form().is_passed():
            return self.json(self.get_form().get_errors())

        result = self.__settings_module.update_options({
            "app_name": self.get_form().get_sinput("app_name"),
            "app_email": self.get_form().get_sinput("app_email"),
            "app_url": self.get_form().get_sinput("app_url"),
            "app_description": self.get_form().get_sinput("app_description"),
            "google_analytics_account": self.get_form().get_sinput("google_analytics_account"),
            "reset_mails_messages_count": self.get_form().get_sinput("reset_mails_messages_count"),
            "reset_mails_expire_after": self.get_form().get_sinput("reset_mails_expire_after"),
            "access_tokens_expire_after": self.get_form().get_sinput("access_tokens_expire_after"),
            "prometheus_token": self.get_form().get_sinput("prometheus_token"),
            "newrelic_api_key":  self.get_form().get_sinput("newrelic_api_key")
        })

        if result:

            self.__activity_module.track(request.user.id, _('You updated application settings.'))

            return self.json([{
                "type": "success",
                "message": _("Settings updated successfully.")
            }])

        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating settings.")
            }])
