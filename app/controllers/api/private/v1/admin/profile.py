"""
Profile API Endpoint
"""

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
from app.modules.core.profile import Profile as Profile_Module


class Profile(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __profile_module = None
    __correlation_id = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__profile_module = Profile_Module()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__form.add_validator(ExtraRules())

    def post(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__user_id = request.user.id

        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
            "action": ""
        })

        self.__form.add_inputs({
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

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_errors_failure(self.__form.get_errors(), {}, self.__correlation_id))

        if self.__form.get_sinput("action") == "_update_profile":
            return self.__update_profile(request)
        elif self.__form.get_sinput("action") == "_update_password":
            return self.__update_password(request)
        elif self.__form.get_sinput("action") == "_update_access_token":
            return self.__update_access_token(request)
        elif self.__form.get_sinput("action") == "_update_refresh_token":
            return self.__update_refresh_token(request)

    def __update_profile(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
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

        self.__form.add_inputs({
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
            'email': {
                'value': request_data["email"],
                'sanitize': {
                    'escape': {},
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
                    'escape': {},
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
                    'escape': {},
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
                    'escape': {},
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

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_errors_failure(self.__form.get_errors(), {}, self.__correlation_id))

        if self.__profile_module.username_used_elsewhere(self.__user_id, self.__form.get_sinput("username")):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Username is already used.")
            }], {}, self.__correlation_id))

        if self.__profile_module.email_used_elsewhere(self.__user_id, self.__form.get_sinput("email")):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Email is already used.")
            }], {}, self.__correlation_id))

        result = self.__profile_module.update_profile(self.__user_id, {
            "first_name": self.__form.get_sinput("first_name"),
            "last_name": self.__form.get_sinput("last_name"),
            "username": self.__form.get_sinput("username"),
            "email": self.__form.get_sinput("email"),
            "job_title": self.__form.get_sinput("job_title"),
            "company": self.__form.get_sinput("company"),
            "address": self.__form.get_sinput("address"),
            "github_url": self.__form.get_sinput("github_url"),
            "twitter_url": self.__form.get_sinput("twitter_url"),
            "facebook_url": self.__form.get_sinput("facebook_url")
        })

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Profile updated successfully.")
            }], {}, self.__correlation_id))

        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating your profile.")
            }], {}, self.__correlation_id))

    def __update_password(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
            "old_password": "",
            "new_password": ""
        })

        self.__form.add_inputs({
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

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_errors_failure(self.__form.get_errors(), {}, self.__correlation_id))

        if not self.__profile_module.validate_password(self.__user_id, self.__form.get_sinput("old_password")):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Old password is invalid.")
            }], {}, self.__correlation_id))

        result = self.__profile_module.change_password(self.__user_id, self.__form.get_sinput("new_password"))

        if result:
            self.__profile_module.restore_session(self.__user_id, request)
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Password updated successfully.")
            }], {}, self.__correlation_id))

        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating your password.")
            }], {}, self.__correlation_id))

    def __update_access_token(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
            "token": "",
        })

        self.__form.add_inputs({
            'token': {
                'value': request_data["token"],
                'validate': {
                    'sv_token': {
                        'error': _("Error! The provided token invalid, Please refresh the page.")
                    }
                }
            }
        })

        self.__form.process()

        if not self.__form.is_passed() and request_data["token"] != "":
            return JsonResponse(self.__response.send_errors_failure(self.__form.get_errors(), {}, self.__correlation_id))

        result = self.__profile_module.update_access_token(self.__user_id)

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Access token updated successfully.")
            }], {"token": result}, self.__correlation_id))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating access token.")
            }], {}, self.__correlation_id))

    def __update_refresh_token(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
            "token": "",
        })

        self.__form.add_inputs({
            'token': {
                'value': request_data["token"],
                'validate': {
                    'sv_token': {
                        'error': _("Error! The provided token invalid, Please refresh the page.")
                    }
                }
            }
        })

        self.__form.process()

        if not self.__form.is_passed() and request_data["token"] != "":
            return JsonResponse(self.__response.send_errors_failure(self.__form.get_errors(), {}, self.__correlation_id))

        result = self.__profile_module.update_refresh_token(self.__user_id)

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Refresh token updated successfully.")
            }], {"token": result}, self.__correlation_id))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating refresh token.")
            }], {}, self.__correlation_id))
