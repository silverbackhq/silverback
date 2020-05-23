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
from app.modules.core.component_group import ComponentGroup as ComponentGroupModule


class ComponentGroups(View, Controller):
    """Create and List Component Groups Private Endpoint Controller"""

    def __init__(self):
        self.__component_group = ComponentGroupModule()

    @allow_if_authenticated
    def post(self, request):

        request_data = self.get_request_data(request, "post", {
            "name": "",
            "description": "",
            "uptime": "",
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
            }
        })

        self.form().process()

        if not self.form().is_passed():
            return self.json(self.form().get_errors())

        # Check if group name not used
        if self.__component_group.get_one_by_name(self.form().get_sinput("name")):
            return self.json([{
                "type": "error",
                "message": _("Error! Component group name is used before.")
            }])

        result = self.__component_group.insert_one({
            "name": self.form().get_sinput("name"),
            "description": self.form().get_sinput("description"),
            "uptime": self.form().get_sinput("uptime")
        })

        if result:
            return self.json([{
                "type": "success",
                "message": _("Component group created successfully.")
            }])
        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while creating group.")
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
            'groups': self.__format_groups(self.__component_group.get_all(offset, limit)),
            'metadata': {
                'offset': offset,
                'limit': limit,
                'count': self.__component_group.count_all()
            }
        })

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


class ComponentGroup(View, Controller):
    """Update and Delete Component Group Private Endpoint Controller"""

    def __init__(self):
        self.__component_group = ComponentGroupModule()

    @allow_if_authenticated
    def post(self, request, group_id):

        request_data = self.get_request_data(request, "post", {
            "name": "",
            "description": "",
            "uptime": ""
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
            }
        })

        self.form().process()

        if not self.form().is_passed():
            return self.json(self.form().get_errors())

        # Check if group name not used elsewhere
        current_group = self.__component_group.get_one_by_name(self.form().get_sinput("name"))

        if current_group and not current_group["id"] == group_id:
            return self.json([{
                "type": "error",
                "message": _("Error! Component group name is used before.")
            }])

        result = self.__component_group.update_one_by_id(group_id, {
            "name": self.form().get_sinput("name"),
            "description": self.form().get_sinput("description"),
            "uptime": self.form().get_sinput("uptime")
        })

        if result:
            return self.json([{
                "type": "success",
                "message": _("Component group updated successfully.")
            }])
        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating group.")
            }])

    @allow_if_authenticated
    def delete(self, request, group_id):

        self.__user_id = request.user.id

        if self.__component_group.delete_one_by_id(group_id):
            return self.json([{
                "type": "success",
                "message": _("Component group deleted successfully.")
            }])

        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while deleting group.")
            }])
