"""
Component Groups API Endpoint
"""

# Django
from django.views import View
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.urls import reverse

# local Django
from pyvalitron.form import Form
from app.modules.validation.extension import ExtraRules
from app.modules.util.helpers import Helpers
from app.modules.core.request import Request
from app.modules.core.response import Response
from app.modules.core.component_group import Component_Group as Component_Group_Module


class Component_Groups(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __component_group = None
    __correlation_id = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__component_group = Component_Group_Module()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__form.add_validator(ExtraRules())

    def post(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"]
        self.__request.set_request(request)

        request_data = self.__request.get_request_data("post", {
            "name": "",
            "description": "",
            "uptime": "",
        })

        self.__form.add_inputs({
            'name': {
                'value': request_data["name"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [1, 90],
                        'error': _('Error! Component group name must be 1 to 90 characters long.')
                    }
                }
            },
            'description': {
                'value': request_data["description"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {}
            },
            'uptime': {
                'value': request_data["uptime"],
                'validate': {
                    'any_of': {
                        'param': [["on", "off"]],
                        'error': _('Error! Uptime is invalid.')
                    }
                }
            }
        })

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_errors_failure(self.__form.get_errors(), {}, self.__correlation_id))

        result = self.__component_group.insert_one({
            "name": self.__form.get_sinput("name"),
            "description": self.__form.get_sinput("description"),
            "uptime": self.__form.get_sinput("uptime")
        })

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Component group created successfully.")
            }], {}, self.__correlation_id))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while creating group.")
            }], {}, self.__correlation_id))

    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"]
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
            'groups': self.__format_groups(self.__component_group.get_all(offset, limit)),
            'metadata': {
                'offset': offset,
                'limit': limit,
                'count': self.__component_group.count_all()
            }
        }, self.__correlation_id))

    def __format_groups(self, groups):
        groups_list = []

        for group in groups:
            groups_list.append({
                "id": group.id,
                "name": group.name,
                "description": group.description,
                "components": self.__component_group.count_components(group.id),
                "created_at": group.created_at.strftime("%b %d %Y %H:%M:%S"),
                "edit_url": reverse("app.web.admin.component_group.edit", kwargs={'group_id': group.id}),
                "delete_url": reverse("app.api.private.v1.admin.component_group.endpoint", kwargs={'group_id': group.id})
            })

        return groups_list


class Component_Group(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __component_group = None
    __correlation_id = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__component_group = Component_Group_Module()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__form.add_validator(ExtraRules())

    def post(self, request, group_id):

        self.__correlation_id = request.META["X-Correlation-ID"]
        self.__request.set_request(request)

        request_data = self.__request.get_request_data("post", {
            "name": "",
            "description": "",
            "uptime": ""
        })

        self.__form.add_inputs({
            'name': {
                'value': request_data["name"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [1, 90],
                        'error': _('Error! Component group name must be 1 to 90 characters long.')
                    }
                }
            },
            'description': {
                'value': request_data["description"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {}
            },
            'uptime': {
                'value': request_data["uptime"],
                'validate': {
                    'any_of': {
                        'param': [["on", "off"]],
                        'error': _('Error! Uptime is invalid.')
                    }
                }
            }
        })

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_errors_failure(self.__form.get_errors(), {}, self.__correlation_id))

        result = self.__component_group.update_one_by_id(group_id, {
            "name": self.__form.get_sinput("name"),
            "description": self.__form.get_sinput("description"),
            "uptime": self.__form.get_sinput("uptime")
        })

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Component group updated successfully.")
            }], {}, self.__correlation_id))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating group.")
            }], {}, self.__correlation_id))

    def delete(self, request, group_id):

        self.__correlation_id = request.META["X-Correlation-ID"]
        self.__user_id = request.user.id

        if self.__component_group.delete_one_by_id(group_id):
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Component group deleted successfully.")
            }], {}, self.__correlation_id))

        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while deleting group.")
            }], {}, self.__correlation_id))
