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
from app.modules.core.component import Component as ComponentModule
from app.modules.core.component_group import ComponentGroup as ComponentGroupModule


class Components(View):
    """Create and List Components Private Endpoint Controller"""

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__component = ComponentModule()
        self.__component_group = ComponentGroupModule()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__form.add_validator(ExtraRules())
        self.__user_id = None
        self.__correlation_id = ""

    @allow_if_authenticated
    def post(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
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
                        'param': [1, 60],
                        'error': _('Error! Component name must be 1 to 60 characters long.')
                    }
                }
            },
            'description': {
                'value': request_data["description"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [0, 150],
                        'error': _('Error! Component name description must be less than 150 characters long.')
                    },
                    'optional': {}
                }
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
                'value': int(request_data["group"]),
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'greater_than': {
                        'error': _('Error! Component group is invalid.'),
                        'param': [0]
                    },
                    'optional': {}
                }
            }
        })

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_errors_failure(self.__form.get_errors(), {}, self.__correlation_id))

        # Check if component name not used
        if self.__component.get_one_by_name(self.__form.get_sinput("name")):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Component name is used before.")
            }], {}, self.__correlation_id))

        # Check if group id is valid
        if self.__form.get_sinput("group") and not self.__component_group.get_one_by_id(self.__form.get_sinput("group")):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Component group is invalid.")
            }], {}, self.__correlation_id))

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
            }], {}, self.__correlation_id))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while creating component.")
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
            'components': self.__format_components(self.__component.get_all(offset, limit)),
            'metadata': {
                'offset': offset,
                'limit': limit,
                'count': self.__component.count_all()
            }
        }, self.__correlation_id))

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
    """Update and Delete Component Private Endpoint Controller"""

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__component = ComponentModule()
        self.__component_group = ComponentGroupModule()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__form.add_validator(ExtraRules())
        self.__user_id = None
        self.__correlation_id = ""

    @allow_if_authenticated
    def post(self, request, component_id):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
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
                        'param': [1, 60],
                        'error': _('Error! Component name must be 1 to 60 characters long.')
                    }
                }
            },
            'description': {
                'value': request_data["description"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [0, 150],
                        'error': _('Error! Component name description must be less than 150 characters long.')
                    },
                    'optional': {}
                }
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
                'value': int(request_data["group"]),
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'greater_than': {
                        'error': _('Error! Component group is invalid.'),
                        'param': [0]
                    },
                    'optional': {}
                }
            }
        })

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_errors_failure(self.__form.get_errors(), {}, self.__correlation_id))

        # Check if component name not used elsewhere
        current_component = self.__component.get_one_by_name(self.__form.get_sinput("name"))

        if current_component and not current_component["id"] == component_id:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Component name is used before.")
            }], {}, self.__correlation_id))

        # Check if group id is valid
        if self.__form.get_sinput("group") and not self.__component_group.get_one_by_id(self.__form.get_sinput("group")):
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Component group is invalid.")
            }], {}, self.__correlation_id))

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
            }], {}, self.__correlation_id))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating component.")
            }], {}, self.__correlation_id))

    @allow_if_authenticated
    def delete(self, request, component_id):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__user_id = request.user.id

        if self.__component.delete_one_by_id(component_id):
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Component deleted successfully.")
            }], {}, self.__correlation_id))

        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while deleting component.")
            }], {}, self.__correlation_id))
