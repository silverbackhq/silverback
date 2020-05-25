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
from django.forms.fields import DateTimeField
from django.utils.translation import gettext as _

# Local Library
from app.controllers.controller import Controller
from app.modules.core.decorators import allow_if_authenticated
from app.modules.core.incident import Incident as IncidentModule


class Incidents(View, Controller):
    """Create and List Incidents Private Endpoint Controller"""

    def __init__(self):
        self.__incident = IncidentModule()

    @allow_if_authenticated
    def post(self, request):

        request_data = self.get_request_data(request, "post", {
            "name": "",
            "status": "",
            "datetime": "",
        })

        self.form().add_inputs({
            'name': {
                'value': request_data["name"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [1, 200],
                        'error': _('Error! Incident name must be 1 to 200 characters long.')
                    }
                }
            },
            'datetime': {
                'value': request_data["datetime"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'sv_datetime': {
                        'error': _('Error! Datetime is invalid.')
                    }
                }
            },
            'status': {
                'value': request_data["status"],
                'validate': {
                    'any_of': {
                        'param': [["open", "closed"]],
                        'error': _('Error! Incident is invalid.')
                    }
                }
            }
        })

        self.form().process()

        if not self.form().is_passed():
            return self.json(self.form().get_errors())

        result = self.__incident.insert_one({
            "name": self.form().get_sinput("name"),
            "status": self.form().get_sinput("status"),
            "datetime": DateTimeField().clean(self.form().get_sinput("datetime")),
            "uri": self.__incident.generate_uri(6)
        })

        if result:
            return self.json([{
                "type": "success",
                "message": _("Incident created successfully.")
            }])
        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while creating incident.")
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
            'incidents': self.__format_incidents(self.__incident.get_all(offset, limit)),
            'metadata': {
                'offset': offset,
                'limit': limit,
                'count': self.__incident.count_all()
            }
        })

    def __format_incidents(self, incidents):
        incidents_list = []

        for incident in incidents:
            incidents_list.append({
                "id": incident.id,
                "name": incident.name,
                "uri": incident.uri,
                "status": incident.status.title(),
                "created_at": incident.created_at.strftime("%b %d %Y %H:%M:%S"),
                "view_url": reverse("app.web.admin.incident.view", kwargs={'incident_id': incident.id}),
                "view_status_url": reverse("app.web.status_page_single", kwargs={'uri': incident.uri}),
                "edit_url": reverse("app.web.admin.incident.edit", kwargs={'incident_id': incident.id}),
                "delete_url": reverse("app.api.private.v1.admin.incident.endpoint", kwargs={'incident_id': incident.id})
            })

        return incidents_list


class Incident(View, Controller):
    """Update Incident Private Endpoint Controller"""

    def __init__(self):
        self.__incident = IncidentModule()

    @allow_if_authenticated
    def post(self, request, incident_id):

        request_data = self.get_request_data(request, "post", {
            "name": "",
            "status": "",
            "datetime": "",
        })

        self.form().add_inputs({
            'name': {
                'value': request_data["name"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [1, 200],
                        'error': _('Error! Incident name must be 1 to 200 characters long.')
                    }
                }
            },
            'datetime': {
                'value': request_data["datetime"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'sv_datetime': {
                        'error': _('Error! Datetime is invalid.')
                    }
                }
            },
            'status': {
                'value': request_data["status"],
                'validate': {
                    'any_of': {
                        'param': [["open", "closed"]],
                        'error': _('Error! Incident is invalid.')
                    }
                }
            }
        })

        self.form().process()

        if not self.form().is_passed():
            return self.json(self.form().get_errors())

        result = self.__incident.update_one_by_id(incident_id, {
            "name": self.form().get_sinput("name"),
            "status": self.form().get_sinput("status"),
            "datetime": DateTimeField().clean(self.form().get_sinput("datetime"))
        })

        if result:
            return self.json([{
                "type": "success",
                "message": _("Incident updated successfully.")
            }])
        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating incident.")
            }])

    @allow_if_authenticated
    def delete(self, request, incident_id):

        if self.__incident.delete_one_by_id(incident_id):
            return self.json([{
                "type": "success",
                "message": _("Incident deleted successfully.")
            }])
        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while deleting incident.")
            }])
