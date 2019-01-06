"""
User API Endpoint
"""

# Django
from django.views import View
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.urls import reverse

# local Django
from app.modules.validation.form import Form
from app.modules.util.helpers import Helpers
from app.modules.core.request import Request
from app.modules.core.response import Response
from app.modules.core.metric import Metric as Metric_Module


class Metrics(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __metric = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__metric = Metric_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def post(self, request):

        self.__request.set_request(request)

        request_data = self.__request.get_request_data("post", {
            "title": "",
            "type": ""
        })

        self.__form.add_inputs({
            'title': {
                'value': request_data["title"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {}
            },
            'type': {
                'value': request_data["type"],
                'validate': {
                    'any_of': {
                        'param': [["graphite", "prometheus"]],
                        'error': _('Error! Type is invalid.')
                    }
                }
            }
        })

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_private_failure(self.__form.get_errors(with_type=True)))

        result = self.__metric.insert_one({
            "title": self.__form.get_input_value("title"),
            "type": self.__form.get_input_value("type"),
            "source": "{}"
        })

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Metric created successfully.")
            }]))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while creating metric.")
            }]))

    def get(self, request):

        self.__request.set_request(request)

        request_data = self.__request.get_request_data("get", {
            "offset": "",
            "limit": ""
        })

        try:
            offset = int(request_data["offset"])
            limit = int(request_data["limit"])
        except Exception:
            offset = 0
            limit = 0

        return JsonResponse(self.__response.send_private_success([], {
            'metrics': self.__format_metrics(self.__metric.get_all(offset, limit)),
            'metadata': {
                'offset': offset,
                'limit': limit,
                'count': self.__metric.count_all()
            }
        }))

    def __format_metrics(self, metrics):
        metrics_list = []

        for metric in metrics:
            metrics_list.append({
                "id": metric.id,
                "title": metric.title,
                "type": metric.type.title(),
                "created_at": metric.created_at.strftime("%b %d %Y %H:%M:%S"),
                "edit_url": reverse("app.web.admin.metric.edit", kwargs={'metric_id': metric.id}),
                "delete_url": reverse("app.api.private.v1.admin.metric.endpoint", kwargs={'metric_id': metric.id})
            })

        return metrics_list


class Metric(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __metric = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__metric = Metric_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def post(self, request, metric_id):

        self.__request.set_request(request)

        request_data = self.__request.get_request_data("post", {
            "title": "",
            "type": ""
        })

        self.__form.add_inputs({
            'title': {
                'value': request_data["title"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {}
            },
            'type': {
                'value': request_data["type"],
                'validate': {
                    'any_of': {
                        'param': [["graphite", "prometheus"]],
                        'error': _('Error! Type is invalid.')
                    }
                }
            }
        })

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_private_failure(self.__form.get_errors(with_type=True)))

        result = self.__metric.update_one_by_id(metric_id, {
            "title": self.__form.get_input_value("title"),
            "type": self.__form.get_input_value("type"),
            "source": "{}"
        })

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Metric updated successfully.")
            }]))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating metric.")
            }]))

    def delete(self, request, metric_id):

        self.__user_id = request.user.id

        if self.__metric.delete_one_by_id(metric_id):
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Metric deleted successfully.")
            }]))

        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while deleting metric.")
            }]))
