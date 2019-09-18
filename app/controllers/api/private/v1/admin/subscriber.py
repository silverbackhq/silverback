"""
    Subscriber API Endpoint
    ~~~~~~~~~~~~~~

    :copyright: silverbackhq
    :license: BSD-3-Clause
"""

# Third Party Library
from django.views import View
from django.urls import reverse
from pyvalitron.form import Form
from django.http import JsonResponse
from django.utils.translation import gettext as _

# Local Library
from app.modules.util.helpers import Helpers
from app.modules.core.request import Request
from app.modules.core.response import Response
from app.modules.validation.extension import ExtraRules
from app.modules.core.decorators import allow_if_authenticated
from app.modules.core.subscriber import Subscriber as SubscriberModule


class Subscribers(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __subscriber = None
    __correlation_id = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__subscriber = SubscriberModule()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__form.add_validator(ExtraRules())

    @allow_if_authenticated
    def post(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__request.set_request(request)

        request_data = self.__request.get_request_data("post", {
            "type": "",
            "email": "",
            "phone": "",
            "endpoint": "",
            "auth_token": "",
            "status": ""
        })

        if request_data["type"] == "email":

            self.__form.add_inputs({
                'type': {
                    'value': request_data["type"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["email", "phone", "endpoint"]],
                            'error': _('Error! Type is invalid.')
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
                            'error': _('Error! Email is invalid.')
                        }
                    }
                },
                'status': {
                    'value': request_data["status"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["pending", "verified", "unverified"]],
                            'error': _('Error! Status is invalid.')
                        }
                    }
                }
            })

        elif request_data["type"] == "phone":

            self.__form.add_inputs({
                'type': {
                    'value': request_data["type"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["email", "phone", "endpoint"]],
                            'error': _('Error! Type is invalid.')
                        }
                    }
                },
                'phone': {
                    'value': request_data["phone"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'sv_phone': {
                            'error': _('Error! Phone number is invalid.')
                        }
                    }
                },
                'status': {
                    'value': request_data["status"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["pending", "verified", "unverified"]],
                            'error': _('Error! Status is invalid.')
                        }
                    }
                }
            })

        else:

            self.__form.add_inputs({
                'type': {
                    'value': request_data["type"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["email", "phone", "endpoint"]],
                            'error': _('Error! Type is invalid.')
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
                            'error': _('Error! Email is invalid.')
                        }
                    }
                },
                'endpoint': {
                    'value': request_data["endpoint"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'sv_url': {
                            'error': _('Error! Endpoint URL is invalid.')
                        }
                    }
                },
                # @TODO add validate filter
                'auth_token': {
                    'value': request_data["auth_token"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {}
                },
                'status': {
                    'value': request_data["status"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["pending", "verified", "unverified"]],
                            'error': _('Error! Status is invalid.')
                        }
                    }
                }
            })

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_errors_failure(self.__form.get_errors(), {}, self.__correlation_id))

        external_id = self.__helpers.generate_uuid()

        while self.__subscriber.get_one_by_external_id(external_id) is not False:
            external_id = self.__helpers.generate_uuid()

        if request_data["type"] == "email":

            result = self.__subscriber.insert_one({
                "status": self.__form.get_sinput("status"),
                "type": self.__form.get_sinput("type"),
                "email": self.__form.get_sinput("email"),
                "phone": "",
                "endpoint": "",
                "auth_token": "",
                "external_id": external_id
            })

        elif request_data["type"] == "phone":

            result = self.__subscriber.insert_one({
                "status": self.__form.get_sinput("status"),
                "type": self.__form.get_sinput("type"),
                "email": "",
                "phone": self.__form.get_sinput("phone"),
                "endpoint": "",
                "auth_token": "",
                "external_id": external_id
            })

        else:

            result = self.__subscriber.insert_one({
                "status": self.__form.get_sinput("status"),
                "type": self.__form.get_sinput("type"),
                "email": self.__form.get_sinput("email"),
                "phone": "",
                "endpoint": self.__form.get_sinput("endpoint"),
                "auth_token": self.__form.get_sinput("auth_token"),
                "external_id": external_id
            })

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Subscriber created successfully.")
            }], {}, self.__correlation_id))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while creating subscriber.")
            }], {}, self.__correlation_id))

    @allow_if_authenticated
    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__request.set_request(request)

        request_data = self.__request.get_request_data("get", {
            "offset": 0,
            "limit": 20
        })

        try:
            offset = int(request_data["offset"])
            limit = int(request_data["limit"])
        except Exception:
            offset = 0
            limit = 20

        return JsonResponse(self.__response.send_private_success([], {
            'subscribers': self.__format_subscribers(self.__subscriber.get_all(offset, limit)),
            'metadata': {
                'offset': offset,
                'limit': limit,
                'count': self.__subscriber.count_all()
            }
        }, self.__correlation_id))

    def __format_subscribers(self, subscribers):
        subscribers_list = []

        for subscriber in subscribers:
            subscribers_list.append({
                "id": subscriber.id,
                "status": subscriber.status.title(),
                "type": subscriber.type,
                "email": subscriber.email,
                "phone": subscriber.phone,
                "endpoint": subscriber.endpoint,
                "auth_token": subscriber.auth_token,
                "created_at": subscriber.created_at.strftime("%b %d %Y %H:%M:%S"),
                "edit_url": reverse("app.web.admin.subscriber.edit", kwargs={'subscriber_id': subscriber.id}),
                "delete_url": reverse("app.api.private.v1.admin.subscriber.endpoint", kwargs={'subscriber_id': subscriber.id})
            })

        return subscribers_list


class Subscriber(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __subscriber = None
    __correlation_id = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__subscriber = SubscriberModule()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__form.add_validator(ExtraRules())

    @allow_if_authenticated
    def post(self, request, subscriber_id):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__request.set_request(request)

        request_data = self.__request.get_request_data("post", {
            "type": "",
            "email": "",
            "phone": "",
            "endpoint": "",
            "auth_token": "",
            "status": ""
        })

        if request_data["type"] == "email":

            self.__form.add_inputs({
                'type': {
                    'value': request_data["type"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["email", "phone", "endpoint"]],
                            'error': _('Error! Type is invalid.')
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
                            'error': _('Error! Email is invalid.')
                        }
                    }
                },
                'status': {
                    'value': request_data["status"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["pending", "verified", "unverified"]],
                            'error': _('Error! Status is invalid.')
                        }
                    }
                }
            })

        elif request_data["type"] == "phone":

            self.__form.add_inputs({
                'type': {
                    'value': request_data["type"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["email", "phone", "endpoint"]],
                            'error': _('Error! Type is invalid.')
                        }
                    }
                },
                'phone': {
                    'value': request_data["phone"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'sv_phone': {
                            'error': _('Error! Phone number is invalid.')
                        }
                    }
                },
                'status': {
                    'value': request_data["status"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["pending", "verified", "unverified"]],
                            'error': _('Error! Status is invalid.')
                        }
                    }
                }
            })

        else:

            self.__form.add_inputs({
                'type': {
                    'value': request_data["type"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["email", "phone", "endpoint"]],
                            'error': _('Error! Type is invalid.')
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
                            'error': _('Error! Email is invalid.')
                        }
                    }
                },
                'endpoint': {
                    'value': request_data["endpoint"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'sv_url': {
                            'error': _('Error! Endpoint URL is invalid.')
                        }
                    }
                },
                # @TODO add validate filter
                'auth_token': {
                    'value': request_data["auth_token"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {}
                },
                'status': {
                    'value': request_data["status"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {
                        'any_of': {
                            'param': [["pending", "verified", "unverified"]],
                            'error': _('Error! Status is invalid.')
                        }
                    }
                }
            })

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_errors_failure(self.__form.get_errors(), {}, self.__correlation_id))

        if request_data["type"] == "email":

            result = self.__subscriber.update_one_by_id(subscriber_id, {
                "status": self.__form.get_sinput("status"),
                "type": self.__form.get_sinput("type"),
                "email": self.__form.get_sinput("email"),
                "phone": "",
                "endpoint": "",
                "auth_token": ""
            })

        elif request_data["type"] == "phone":

            result = self.__subscriber.update_one_by_id(subscriber_id, {
                "status": self.__form.get_sinput("status"),
                "type": self.__form.get_sinput("type"),
                "email": "",
                "phone": self.__form.get_sinput("phone"),
                "endpoint": "",
                "auth_token": ""
            })

        else:

            result = self.__subscriber.update_one_by_id(subscriber_id, {
                "status": self.__form.get_sinput("status"),
                "type": self.__form.get_sinput("type"),
                "email": self.__form.get_sinput("email"),
                "phone": "",
                "endpoint": self.__form.get_sinput("endpoint"),
                "auth_token": self.__form.get_sinput("auth_token")
            })

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Subscriber updated successfully.")
            }], {}, self.__correlation_id))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating subscriber.")
            }], {}, self.__correlation_id))

    @allow_if_authenticated
    def delete(self, request, subscriber_id):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__user_id = request.user.id

        if self.__subscriber.delete_one_by_id(subscriber_id):
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Subscriber deleted successfully.")
            }], {}, self.__correlation_id))

        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while deleting subscriber.")
            }], {}, self.__correlation_id))
