"""
Component API Endpoint
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
from app.modules.core.component import Component as Component_Module


class Components(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __component = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__component = Component_Module()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__form.add_validator(ExtraRules())

    def post(self, request):

        self.__request.set_request(request)

        request_data = self.__request.get_request_data("post", {
            "name": "",
            "description": "",
            "uptime": "",
            "group": ""
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
                        'error': _('Error! Component name must be 1 to 90 characters long.')
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
            },
            'group': {
                'value': request_data["group"],
                'sanitize': {},
                'validate': {}
            }
        })

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_errors_failure(self.__form.get_errors()))

        result = self.__component.insert_one({
            "name": self.__form.get_sinput("name"),
            "description": self.__form.get_sinput("description"),
            "uptime": self.__form.get_sinput("uptime"),
            "group_id": None if self.__form.get_sinput("group") == "" else self.__form.get_sinput("group")
        })

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Component created successfully.")
            }]))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while creating component.")
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
            'components': self.__format_components(self.__component.get_all(offset, limit)),
            'metadata': {
                'offset': offset,
                'limit': limit,
                'count': self.__component.count_all()
            }
        }))

    def __format_components(self, components):
        components_list = []

        for component in components:
            components_list.append({
                "id": component.id,
                "name": component.name,
                "description": component.description,
                "uptime": component.uptime,
                "group": "---" if component.group is None else component.group.name,
                "created_at": component.created_at.strftime("%b %d %Y %H:%M:%S"),
                "edit_url": reverse("app.web.admin.component.edit", kwargs={'component_id': component.id}),
                "delete_url": reverse("app.api.private.v1.admin.component.endpoint", kwargs={'component_id': component.id})
            })

        return components_list


class Component(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __component = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__component = Component_Module()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__form.add_validator(ExtraRules())

    def post(self, request, component_id):

        self.__request.set_request(request)

        request_data = self.__request.get_request_data("post", {
            "name": "",
            "description": "",
            "uptime": "",
            "group": ""
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
                        'error': _('Error! Component name must be 1 to 90 characters long.')
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
            },
            'group': {
                'value': request_data["group"],
                'sanitize': {},
                'validate': {}
            }
        })

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_errors_failure(self.__form.get_errors()))

        result = self.__component.update_one_by_id(component_id, {
            "name": self.__form.get_sinput("name"),
            "description": self.__form.get_sinput("description"),
            "uptime": self.__form.get_sinput("uptime"),
            "group_id": None if self.__form.get_sinput("group") == "" else self.__form.get_sinput("group")
        })

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Component updated successfully.")
            }]))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating component.")
            }]))

    def delete(self, request, component_id):

        self.__user_id = request.user.id

        if self.__component.delete_one_by_id(component_id):
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Component deleted successfully.")
            }]))

        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while deleting component.")
            }]))
