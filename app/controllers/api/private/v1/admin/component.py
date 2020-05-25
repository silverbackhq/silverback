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
from django.utils.translation import gettext as _

# Local Library
from app.controllers.controller import Controller
from app.modules.core.decorators import allow_if_authenticated
from app.modules.core.component import Component as ComponentModule
from app.modules.core.component_group import ComponentGroup as ComponentGroupModule


class Components(View, Controller):
    """Create and List Components Private Endpoint Controller"""

    def __init__(self):
        self.__component = ComponentModule()
        self.__component_group = ComponentGroupModule()

    @allow_if_authenticated
    def post(self, request):

        request_data = self.get_request_data(request, "post", {
            "name": "",
            "description": "",
            "uptime": "",
            "group": ""
        })

        self.form().add_inputs({
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

        self.form().process()

        if not self.form().is_passed():
            return self.json(self.form().get_errors())

        # Check if component name not used
        if self.__component.get_one_by_name(self.form().get_sinput("name")):
            return self.json([{
                "type": "error",
                "message": _("Error! Component name is used before.")
            }])

        # Check if group id is valid
        if self.form().get_sinput("group") and not self.__component_group.get_one_by_id(self.form().get_sinput("group")):
            return self.json([{
                "type": "error",
                "message": _("Error! Component group is invalid.")
            }])

        result = self.__component.insert_one({
            "name": self.form().get_sinput("name"),
            "description": self.form().get_sinput("description"),
            "uptime": self.form().get_sinput("uptime"),
            "group_id": None if self.form().get_sinput("group") == "" else self.form().get_sinput("group")
        })

        if result:
            return self.json([{
                "type": "success",
                "message": _("Component created successfully.")
            }])
        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while creating component.")
            }])

    @allow_if_authenticated
    def get(self, request):

        request_data = self.get_request_data(request, "get", {
            "offset": 0,
            "limit": 20
        })

        try:
            offset = int(request_data["offset"])
            limit = int(request_data["limit"])
        except Exception:
            offset = 0
            limit = 20

        return self.json([], {
            'components': self.__format_components(self.__component.get_all(offset, limit)),
            'metadata': {
                'offset': offset,
                'limit': limit,
                'count': self.__component.count_all()
            }
        })

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


class Component(View, Controller):
    """Update and Delete Component Private Endpoint Controller"""

    def __init__(self):
        self.__component = ComponentModule()
        self.__component_group = ComponentGroupModule()

    @allow_if_authenticated
    def post(self, request, component_id):

        request_data = self.get_request_data(request, "post", {
            "name": "",
            "description": "",
            "uptime": "",
            "group": ""
        })

        self.form().add_inputs({
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

        self.form().process()

        if not self.form().is_passed():
            return self.json(self.form().get_errors())

        # Check if component name not used elsewhere
        current_component = self.__component.get_one_by_name(self.form().get_sinput("name"))

        if current_component and not current_component["id"] == component_id:
            return self.json([{
                "type": "error",
                "message": _("Error! Component name is used before.")
            }])

        # Check if group id is valid
        if self.form().get_sinput("group") and not self.__component_group.get_one_by_id(self.form().get_sinput("group")):
            return self.json([{
                "type": "error",
                "message": _("Error! Component group is invalid.")
            }])

        result = self.__component.update_one_by_id(component_id, {
            "name": self.form().get_sinput("name"),
            "description": self.form().get_sinput("description"),
            "uptime": self.form().get_sinput("uptime"),
            "group_id": None if self.form().get_sinput("group") == "" else self.form().get_sinput("group")
        })

        if result:
            return self.json([{
                "type": "success",
                "message": _("Component updated successfully.")
            }])
        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating component.")
            }])

    @allow_if_authenticated
    def delete(self, request, component_id):

        if self.__component.delete_one_by_id(component_id):
            return self.json([{
                "type": "success",
                "message": _("Component deleted successfully.")
            }])

        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while deleting component.")
            }])
