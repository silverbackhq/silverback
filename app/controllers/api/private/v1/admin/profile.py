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
from app.modules.core.profile import Profile as ProfileModule
from app.modules.core.decorators import allow_if_authenticated


class Profile(View, Controller):
    """Update Profile Private Endpoint Controller"""

    def __init__(self):
        self.__profile_module = ProfileModule()

    @allow_if_authenticated
    def post(self, request):

        self.__correlation_id = self.get_correlation(request)
        self.__user_id = request.user.id

        self.get_request().set_request(request)
        request_data = self.get_request().get_request_data("post", {
            "action": ""
        })

        self.get_form().add_inputs({
            'action': {
                'value': request_data["action"],
                'validate': {
                    'any_of': {
                        'param': [["_update_profile", "_update_password", "_update_access_token", "_update_refresh_token"]],
                        'error': _("Error! Invalid Request.")
                    }
                }
            }
        })

        self.get_form().process()

        if not self.get_form().is_passed():
            return self.json(self.get_form().get_errors())

        if self.get_form().get_sinput("action") == "_update_profile":
            return self.__update_profile(request)
        elif self.get_form().get_sinput("action") == "_update_password":
            return self.__update_password(request)
        elif self.get_form().get_sinput("action") == "_update_access_token":
            return self.__update_access_token(request)
        elif self.get_form().get_sinput("action") == "_update_refresh_token":
            return self.__update_refresh_token(request)

    def __update_profile(self, request):

        self.__correlation_id = self.get_correlation(request)
        self.get_request().set_request(request)
        request_data = self.get_request().get_request_data("post", {
            "first_name": "",
            "last_name": "",
            "username": "",
            "email": "",
            "job_title": "",
            "company": "",
            "address": "",
            "github_url": "",
            "twitter_url": "",
            "facebook_url": ""
        })

        self.get_form().add_inputs({
            'first_name': {
                'value': request_data["first_name"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'sv_names': {
                        'error': _('Error! First name contains invalid characters.')
                    },
                    'length_between': {
                        'param': [0, 20],
                        'error': _('Error! First name must be 1 to 20 characters long.')
                    }
                }
            },
            'last_name': {
                'value': request_data["last_name"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'sv_names': {
                        'error': _('Error! Last name contains invalid characters.')
                    },
                    'length_between': {
                        'param': [0, 20],
                        'error': _('Error! Last name must be 1 to 20 characters long.')
                    }
                }
            },
            'username': {
                'value': request_data["username"],
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
            'email': {
                'value': request_data["email"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'sv_email': {
                        'error': _('Error! Admin email is invalid.')
                    }
                }
            },
            'job_title': {
                'value': request_data["job_title"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [0, 80],
                        'error': _('Error! Job title is very long.')
                    },
                    'optional': {}
                }
            },
            'company': {
                'value': request_data["company"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [0, 80],
                        'error': _('Error! Company is very long.')
                    },
                    'optional': {}
                }
            },
            'address': {
                'value': request_data["address"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [0, 80],
                        'error': _('Error! Address is very long.')
                    },
                    'optional': {}
                }
            },
            'github_url': {
                'value': request_data["github_url"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'sv_url': {
                        'error': _('Error! Github url is invalid.')
                    },
                    'length_between': {
                        'param': [0, 80],
                        'error': _('Error! Github url is very long.')
                    },
                    'optional': {}
                }
            },
            'twitter_url': {
                'value': request_data["twitter_url"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'sv_url': {
                        'error': _('Error! Twitter url is invalid.')
                    },
                    'length_between': {
                        'param': [0, 80],
                        'error': _('Error! Twitter url is very long.')
                    },
                    'optional': {}
                }
            },
            'facebook_url': {
                'value': request_data["facebook_url"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'sv_url': {
                        'error': _('Error! Facebook url is invalid.')
                    },
                    'length_between': {
                        'param': [0, 80],
                        'error': _('Error! Facebook url is very long.')
                    },
                    'optional': {}
                }
            }
        })

        self.get_form().process()

        if not self.get_form().is_passed():
            return self.json(self.get_form().get_errors())

        if self.__profile_module.username_used_elsewhere(self.__user_id, self.get_form().get_sinput("username")):
            return self.json([{
                "type": "error",
                "message": _("Error! Username is already used.")
            }])

        if self.__profile_module.email_used_elsewhere(self.__user_id, self.get_form().get_sinput("email")):
            return self.json([{
                "type": "error",
                "message": _("Error! Email is already used.")
            }])

        result = self.__profile_module.update_profile(self.__user_id, {
            "first_name": self.get_form().get_sinput("first_name"),
            "last_name": self.get_form().get_sinput("last_name"),
            "username": self.get_form().get_sinput("username"),
            "email": self.get_form().get_sinput("email"),
            "job_title": self.get_form().get_sinput("job_title"),
            "company": self.get_form().get_sinput("company"),
            "address": self.get_form().get_sinput("address"),
            "github_url": self.get_form().get_sinput("github_url"),
            "twitter_url": self.get_form().get_sinput("twitter_url"),
            "facebook_url": self.get_form().get_sinput("facebook_url")
        })

        if result:
            return self.json([{
                "type": "success",
                "message": _("Profile updated successfully.")
            }])

        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating your profile.")
            }])

    def __update_password(self, request):

        self.__correlation_id = self.get_correlation(request)
        self.get_request().set_request(request)
        request_data = self.get_request().get_request_data("post", {
            "old_password": "",
            "new_password": ""
        })

        self.get_form().add_inputs({
            'old_password': {
                'value': request_data["old_password"],
                'validate': {
                    'sv_password': {
                        'error': _("Error! Old password is invalid.")
                    },
                    'length_between': {
                        'param': [7, 20],
                        'error': _("Error! Old password is invalid.")
                    }
                }
            },
            'new_password': {
                'value': request_data["new_password"],
                'validate': {
                    'sv_password': {
                        'error': _('Error! New Password must contain at least uppercase letter, lowercase letter, numbers and special character.')
                    },
                    'length_between': {
                        'param': [7, 20],
                        'error': _('Error! New Password length must be from 8 to 20 characters.')
                    }
                }
            }
        })

        self.get_form().process()

        if not self.get_form().is_passed():
            return self.json(self.get_form().get_errors())

        if not self.__profile_module.validate_password(self.__user_id, self.get_form().get_sinput("old_password")):
            return self.json([{
                "type": "error",
                "message": _("Error! Old password is invalid.")
            }])

        result = self.__profile_module.change_password(self.__user_id, self.get_form().get_sinput("new_password"))

        if result:
            self.__profile_module.restore_session(self.__user_id, request)
            return self.json([{
                "type": "success",
                "message": _("Password updated successfully.")
            }])

        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating your password.")
            }])

    def __update_access_token(self, request):

        self.__correlation_id = self.get_correlation(request)
        self.get_request().set_request(request)
        request_data = self.get_request().get_request_data("post", {
            "token": "",
        })

        self.get_form().add_inputs({
            'token': {
                'value': request_data["token"],
                'validate': {
                    'sv_token': {
                        'error': _("Error! The provided token invalid, Please refresh the page.")
                    }
                }
            }
        })

        self.get_form().process()

        if not self.get_form().is_passed() and request_data["token"] != "":
            return self.json(self.get_form().get_errors())

        result = self.__profile_module.update_access_token(self.__user_id)

        if result:
            return self.json([{
                "type": "success",
                "message": _("Access token updated successfully.")
            }], {"token": result})
        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating access token.")
            }])

    def __update_refresh_token(self, request):

        self.__correlation_id = self.get_correlation(request)
        self.get_request().set_request(request)
        request_data = self.get_request().get_request_data("post", {
            "token": "",
        })

        self.get_form().add_inputs({
            'token': {
                'value': request_data["token"],
                'validate': {
                    'sv_token': {
                        'error': _("Error! The provided token invalid, Please refresh the page.")
                    }
                }
            }
        })

        self.get_form().process()

        if not self.get_form().is_passed() and request_data["token"] != "":
            return self.json(self.get_form().get_errors())

        result = self.__profile_module.update_refresh_token(self.__user_id)

        if result:
            return self.json([{
                "type": "success",
                "message": _("Refresh token updated successfully.")
            }], {"token": result})
        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating refresh token.")
            }])
