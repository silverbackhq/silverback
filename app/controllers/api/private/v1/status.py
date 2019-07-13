"""
Status Page API Endpoint
"""

# Third Party Library
from django.views import View
from pyvalitron.form import Form
from django.http import JsonResponse
from django.utils.translation import gettext as _

# Local Library
from app.modules.util.helpers import Helpers
from app.modules.core.request import Request
from app.modules.core.response import Response
from app.modules.validation.extension import ExtraRules
from app.modules.core.subscriber import Subscriber as SubscriberModule


class StatusSubscribe(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
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
                'email': {
                    'value': request_data["email"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {}
                }
            })

        elif request_data["type"] == "phone":

            self.__form.add_inputs({
                'phone': {
                    'value': request_data["phone"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {}
                }
            })

        elif request_data["type"] == "endpoint":

            self.__form.add_inputs({
                'email': {
                    'value': request_data["email"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {}
                },
                'endpoint': {
                    'value': request_data["endpoint"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {}
                },
                'auth_token': {
                    'value': request_data["auth_token"],
                    'sanitize': {
                        'strip': {}
                    },
                    'validate': {}
                }
            })

        else:

            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Invalid request.")
            }], {}, self.__correlation_id))

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_errors_failure(self.__form.get_errors(), {}, self.__correlation_id))

        external_id = self.__helpers.generate_uuid()

        while self.__subscriber.get_one_by_external_id(external_id) is not False:
            external_id = self.__helpers.generate_uuid()

        if request_data["type"] == "email":
            result = self.__subscriber.insert_one({
                "status": "pending",
                "type": "email",
                "email": self.__form.get_sinput("email"),
                "phone": "",
                "endpoint": "",
                "auth_token": "",
                "external_id": external_id
            })

        elif request_data["type"] == "phone":
            result = self.__subscriber.insert_one({
                "status": "pending",
                "type": "phone",
                "email": "",
                "phone": self.__form.get_sinput("phone"),
                "endpoint": "",
                "auth_token": "",
                "external_id": external_id
            })

        else:
            result = self.__subscriber.insert_one({
                "status": "pending",
                "type": "endpoint",
                "email": self.__form.get_sinput("email"),
                "phone": "",
                "endpoint": self.__form.get_sinput("endpoint"),
                "auth_token": self.__form.get_sinput("auth_token"),
                "external_id": external_id
            })

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("You have successfully subscribed.")
            }], {}, self.__correlation_id))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while subscribing.")
            }], {}, self.__correlation_id))
