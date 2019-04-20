"""
Builder API Endpoint
"""

import json

# Django
from django.views import View
from django.http import JsonResponse
from django.utils.translation import gettext as _

# local Django
from pyvalitron.form import Form
from app.modules.validation.extension import ExtraRules
from app.modules.util.helpers import Helpers
from app.modules.core.request import Request
from app.modules.core.response import Response
from app.modules.core.settings import Settings


class Builder_System_Metrics(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __settings = None
    __correlation_id = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__settings = Settings()
        self.__form = Form()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__form.add_validator(ExtraRules())

    def post(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
            "metric_id": ""
        })

        metrics = self.__settings.get_value_by_key(
            "builder_metrics",
            json.dumps([])
        )

        metrics = json.loads(metrics)

        if request_data["metric_id"] in metrics:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Metric added successfully.")
            }], {}, self.__correlation_id))

        metrics.append(request_data["metric_id"])

        result = self.__settings.update_options({
            "builder_metrics": json.dumps(metrics)
        })

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Metric added successfully.")
            }], {}, self.__correlation_id))

        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while adding metric.")
            }], {}, self.__correlation_id))

    def delete(self, request, metric_id):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        metrics = self.__settings.get_value_by_key(
            "builder_metrics",
            json.dumps([])
        )

        metrics = json.loads(metrics)

        if metric_id not in metrics:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Metric deleted successfully.")
            }], {}, self.__correlation_id))

        metrics.remove(metric_id)

        result = self.__settings.update_options({
            "builder_metrics": json.dumps(metrics)
        })

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Metric deleted successfully.")
            }], {}, self.__correlation_id))

        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while deleting metric.")
            }], {}, self.__correlation_id))


class Builder_Components(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __settings = None
    __correlation_id = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__settings = Settings()
        self.__form = Form()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__form.add_validator(ExtraRules())

    def post(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
            "component_id": ""
        })

        components = self.__settings.get_value_by_key(
            "builder_components",
            json.dumps([])
        )

        components = json.loads(components)

        if request_data["component_id"] in components:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Component added successfully.")
            }], {}, self.__correlation_id))

        components.append(request_data["component_id"])

        result = self.__settings.update_options({
            "builder_components": json.dumps(components)
        })

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Component added successfully.")
            }], {}, self.__correlation_id))

        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while adding component.")
            }], {}, self.__correlation_id))

    def delete(self, request, component_id):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        components = self.__settings.get_value_by_key(
            "builder_components",
            json.dumps([])
        )

        components = json.loads(components)

        if component_id not in components:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Component deleted successfully.")
            }], {}, self.__correlation_id))

        components.remove(component_id)

        result = self.__settings.update_options({
            "builder_components": json.dumps(components)
        })

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Component deleted successfully.")
            }], {}, self.__correlation_id))

        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while deleting component.")
            }], {}, self.__correlation_id))


class Builder_Settings(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __settings = None
    __correlation_id = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__settings = Settings()
        self.__form = Form()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__form.add_validator(ExtraRules())

    def post(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__request.set_request(request)
        request_data = self.__request.get_request_data("post", {
            "builder_headline": "",
            "builder_favicon_url": "",
            "builder_logo_url": "",
            "builder_about": ""
        })

        self.__form.add_inputs({
            'builder_headline': {
                'value': request_data["builder_headline"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [0, 100],
                        'error': _('Error! Headline is very long.')
                    },
                    'optional': {}
                }
            },
            'builder_favicon_url': {
                'value': request_data["builder_favicon_url"],
                'sanitize': {
                    'escape': {},
                    'strip': {}
                },
                'validate': {
                    'sv_url': {
                        'error': _('Error! Favicon URL is invalid.')
                    }
                }
            },
            'builder_logo_url': {
                'value': request_data["builder_logo_url"],
                'sanitize': {
                    'escape': {},
                    'strip': {}
                },
                'validate': {
                    'sv_url': {
                        'error': _('Error! Logo URL is invalid.')
                    }
                }
            },
            'builder_about': {
                'value': request_data["builder_about"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [0, 20000],
                        'error': _('Error! About is very long.')
                    },
                    'optional': {}
                }
            },
        })

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_errors_failure(self.__form.get_errors(), {}, self.__correlation_id))

        result = self.__settings.update_options({
            "builder_headline": self.__form.get_sinput("builder_headline"),
            "builder_favicon_url": self.__form.get_sinput("builder_favicon_url"),
            "builder_logo_url": self.__form.get_sinput("builder_logo_url"),
            "builder_about": self.__form.get_sinput("builder_about")
        })

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Settings updated successfully.")
            }], {}, self.__correlation_id))

        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating settings.")
            }], {}, self.__correlation_id))
