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
from app.modules.core.task import Task as Task_Module
from app.modules.core.decorators import allow_if_authenticated
from app.modules.core.incident import Incident as IncidentModule
from app.modules.core.subscriber import Subscriber as SubscriberModule
from app.modules.core.notification import Notification as NotificationModule
from app.modules.core.incident_update import IncidentUpdate as IncidentUpdateModule
from app.modules.core.incident_update_component import IncidentUpdateComponent as IncidentUpdateComponentModule
from app.modules.core.incident_update_notification import IncidentUpdateNotification as IncidentUpdateNotificationModule


class IncidentUpdates(View, Controller):
    """Create and List Incident Updates Private Endpoint Controller"""

    def __init__(self):
        self.__incident = IncidentModule()
        self.__incident_update = IncidentUpdateModule()
        self.__task = Task_Module()
        self.__notification = NotificationModule()
        self.__subscriber = SubscriberModule()
        self.__incident_update_notification = IncidentUpdateNotificationModule()

    @allow_if_authenticated
    def post(self, request, incident_id):

        self.__correlation_id = self.get_correlation(request)
        self.__user_id = request.user.id
        self.get_request().set_request(request)

        request_data = self.get_request().get_request_data("post", {
            "status": "",
            "notify_subscribers": "",
            "message": "",
            "datetime": "",
        })

        self.get_form().add_inputs({
            'message': {
                'value': request_data["message"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [1, 3000000],
                        'error': _('Error! Update message must be 1 to 3M characters long.')
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
                        'param': [["investigating", "identified", "monitoring", "update", "resolved"]],
                        'error': _('Error! Status is invalid.')
                    }
                }
            },
            'notify_subscribers': {
                'value': request_data["notify_subscribers"],
                'validate': {
                    'any_of': {
                        'param': [["on", "off"]],
                        'error': _('Error! Notify subscribers is invalid.')
                    }
                }
            }
        })

        self.get_form().process()

        if not self.get_form().is_passed():
            return self.json(self.get_form().get_errors())

        result = self.__incident_update.insert_one({
            "notify_subscribers": self.get_form().get_sinput("notify_subscribers"),
            "datetime": DateTimeField().clean(self.get_form().get_sinput("datetime")),
            "total_suscribers": self.__subscriber.count_by_status(SubscriberModule.VERIFIED),
            "message": self.get_form().get_sinput("message"),
            "status": self.get_form().get_sinput("status"),
            "incident_id": incident_id
        })

        if self.get_form().get_sinput("status") == "resolved":
            self.__incident.update_one_by_id(incident_id, {
                "status": "closed"
            })
        else:
            self.__incident.update_one_by_id(incident_id, {
                "status": "open"
            })

        if result:
            return self.json([{
                "type": "success",
                "message": _("Incident update created successfully.")
            }])
        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while creating update.")
            }])

    @allow_if_authenticated
    def get(self, request, incident_id):

        self.__correlation_id = self.get_correlation(request)
        self.get_request().set_request(request)

        request_data = self.get_request().get_request_data("get", {
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
            'updates': self.__format_incident_updates(self.__incident_update.get_all(incident_id, offset, limit), incident_id),
            'metadata': {
                'offset': offset,
                'limit': limit,
                'count': self.__incident_update.count_all(incident_id)
            }
        })

    def __format_incident_updates(self, updates, incident_id):
        updates_list = []

        for update in updates:

            notified_subscribers = self.__incident_update_notification.count_by_update_status(
                update.id,
                IncidentUpdateNotificationModule.SUCCESS
            )
            progress = int(notified_subscribers/update.total_suscribers) * 100 if update.total_suscribers > 0 else 0

            updates_list.append({
                "id": update.id,
                "status": update.status.title(),
                "notify_subscribers": update.notify_subscribers.title(),
                "datetime": update.datetime.strftime("%b %d %Y %H:%M:%S"),
                "progress": progress if progress <= 100 else 100,
                "created_at": update.created_at.strftime("%b %d %Y %H:%M:%S"),
                "view_url": reverse("app.web.admin.incident_update.view", kwargs={'incident_id': incident_id, "update_id": update.id}),
                "edit_url": reverse("app.web.admin.incident_update.edit", kwargs={'incident_id': incident_id, "update_id": update.id}),
                "delete_url": reverse("app.api.private.v1.admin.incident_update.endpoint", kwargs={'incident_id': incident_id, "update_id": update.id})
            })

        return updates_list


class IncidentUpdate(View, Controller):
    """Update and Delete Incident Update Private Endpoint Controller"""

    def __init__(self):
        self.__incident_update = IncidentUpdateModule()

    @allow_if_authenticated
    def post(self, request, incident_id, update_id):

        self.__correlation_id = self.get_correlation(request)
        self.get_request().set_request(request)

        request_data = self.get_request().get_request_data("post", {
            "status": "",
            "notify_subscribers": "",
            "message": "",
            "datetime": "",
        })

        self.get_form().add_inputs({
            'message': {
                'value': request_data["message"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {
                    'length_between': {
                        'param': [1, 3000000],
                        'error': _('Error! Update message must be 1 to 3M characters long.')
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
                        'param': [["investigating", "identified", "monitoring", "update", "resolved"]],
                        'error': _('Error! Status is invalid.')
                    }
                }
            },
            'notify_subscribers': {
                'value': request_data["notify_subscribers"],
                'validate': {
                    'any_of': {
                        'param': [["on", "off"]],
                        'error': _('Error! Notify subscribers is invalid.')
                    }
                }
            }
        })

        self.get_form().process()

        if not self.get_form().is_passed():
            return self.json(self.get_form().get_errors())

        result = self.__incident_update.update_one_by_id(update_id, {
            "notify_subscribers": self.get_form().get_sinput("notify_subscribers"),
            "datetime": DateTimeField().clean(self.get_form().get_sinput("datetime")),
            "message": self.get_form().get_sinput("message"),
            "status": self.get_form().get_sinput("status")
        })

        if result:
            return self.json([{
                "type": "success",
                "message": _("Incident update updated successfully.")
            }])
        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating update.")
            }])

    @allow_if_authenticated
    def delete(self, request, incident_id, update_id):

        self.__correlation_id = self.get_correlation(request)
        self.__user_id = request.user.id

        if self.__incident_update.delete_one_by_id(update_id):
            return self.json([{
                "type": "success",
                "message": _("Incident update deleted successfully.")
            }])

        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while deleting incident update.")
            }])


class IncidentUpdatesNotify(View, Controller):
    """Notify Subscribers about Incident Update Private Endpoint Controller"""

    def __init__(self):
        self.__incident_update = IncidentUpdateModule()
        self.__task = Task_Module()
        self.__notification = NotificationModule()
        self.__subscriber = SubscriberModule()

    @allow_if_authenticated
    def post(self, request, incident_id, update_id):

        self.__correlation_id = self.get_correlation(request)
        self.__user_id = request.user.id

        task = self.__task.delay("incident_update", {
            "incident_update_id": update_id,
            "user_id": self.__user_id
        }, self.__user_id)

        result = False

        if task:
            result = self.__notification.create_notification({
                "highlight": "Incident Update",
                "notification": "notifying subscribers with the incident update",
                "url": "#",
                "type": NotificationModule.PENDING,
                "delivered": False,
                "user_id": self.__user_id,
                "task_id": task.id
            })

        if task and result:
            return self.json([{
                "type": "success",
                "message": _("Notification delivery started successfully.")
            }])
        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while starting delivery.")
            }])


class IncidentUpdatesComponents(View, Controller):
    """Link Component to Incident Update Private Endpoint Controller"""

    def __init__(self):
        self.__incident_update = IncidentUpdateModule()
        self.__task = Task_Module()
        self.__notification = NotificationModule()
        self.__subscriber = SubscriberModule()
        self.__incident_update_component = IncidentUpdateComponentModule()

    @allow_if_authenticated
    def post(self, request, incident_id, update_id):

        self.__correlation_id = self.get_correlation(request)
        self.__user_id = request.user.id
        self.get_request().set_request(request)

        request_data = self.get_request().get_request_data("post", {
            "type": "",
            "component_id": ""
        })

        self.get_form().add_inputs({
            'component_id': {
                'value': request_data["component_id"],
                'validate': {
                    'sv_numeric': {
                        'error': _('Error! Component is required.')
                    }
                }
            },
            'type': {
                'value': request_data["type"],
                'validate': {
                    'any_of': {
                        'param': [["operational", "degraded_performance", "partial_outage", "major_outage", "maintenance"]],
                        'error': _('Error! Type is required.')
                    }
                }
            }
        })

        self.get_form().process()

        if not self.get_form().is_passed():
            return self.json(self.get_form().get_errors())

        result = self.__incident_update_component.insert_one({
            "component_id": int(self.get_form().get_sinput("component_id")),
            "type": self.get_form().get_sinput("type"),
            "incident_update_id": int(update_id)
        })

        if result:
            return self.json([{
                "type": "success",
                "message": _("Affected component created successfully.")
            }])
        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while creating affected component.")
            }])


class IncidentUpdatesComponent(View, Controller):
    """Remove Component from Incident Update Private Endpoint Controller"""

    def __init__(self):
        self.__incident_update_component = IncidentUpdateComponentModule()

    @allow_if_authenticated
    def delete(self, request, incident_id, update_id, item_id):

        self.__correlation_id = self.get_correlation(request)
        self.__user_id = request.user.id

        if self.__incident_update_component.delete_one_by_id(item_id):
            return self.json([{
                "type": "success",
                "message": _("Affected component deleted successfully.")
            }])

        else:
            return self.json([{
                "type": "error",
                "message": _("Error! Something goes wrong while deleting affected component.")
            }])
