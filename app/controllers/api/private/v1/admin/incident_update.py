"""
User API Endpoint
"""

# Django
from django.views import View
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.urls import reverse
from django.forms.fields import DateTimeField

# local Django
from app.modules.validation.form import Form
from app.modules.util.helpers import Helpers
from app.modules.core.request import Request
from app.modules.core.response import Response
from app.modules.core.task import Task as Task_Module
from app.modules.core.notification import Notification as Notification_Module
from app.modules.core.subscriber import Subscriber as Subscriber_Module
from app.modules.core.incident_update import Incident_Update as Incident_Update_Module
from app.modules.core.incident_update_component import Incident_Update_Component as Incident_Update_Component_Module


class Incident_Updates(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __incident_update = None
    __task = None
    __notification = None
    __subscriber = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__incident_update = Incident_Update_Module()
        self.__task = Task_Module()
        self.__notification = Notification_Module()
        self.__subscriber = Subscriber_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def post(self, request, incident_id):

        self.__user_id = request.user.id

        self.__request.set_request(request)

        request_data = self.__request.get_request_data("post", {
            "status": "",
            "notify_subscribers": "",
            "message": "",
            "datetime": "",
        })

        self.__form.add_inputs({
            'message': {
                'value': request_data["message"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {}
            },
            'datetime': {
                'value': request_data["datetime"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {}
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

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_private_failure(self.__form.get_errors(with_type=True)))

        result = self.__incident_update.insert_one({
            "notify_subscribers": self.__form.get_input_value("notify_subscribers"),
            "datetime": DateTimeField().clean(self.__form.get_input_value("datetime")),
            "total_suscribers": self.__subscriber.count_by_status(Subscriber_Module.VERIFIED),
            "notified_subscribers": 0,
            "failed_subscribers": 0,
            "message": self.__form.get_input_value("message"),
            "status": self.__form.get_input_value("status"),
            "incident_id": incident_id
        })

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Incident update created successfully.")
            }]))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while creating update.")
            }]))

    def get(self, request, incident_id):

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
            'updates': self.__format_incident_updates(self.__incident_update.get_all(incident_id, offset, limit), incident_id),
            'metadata': {
                'offset': offset,
                'limit': limit,
                'count': self.__incident_update.count_all(incident_id)
            }
        }))

    def __format_incident_updates(self, updates, incident_id):
        updates_list = []

        for update in updates:
            updates_list.append({
                "id": update.id,
                "status": update.status.title(),
                "notify_subscribers": update.notify_subscribers.title(),
                "datetime": update.datetime.strftime("%b %d %Y %H:%M:%S"),
                "progress": int(update.notified_subscribers/update.total_suscribers) * 100 if update.total_suscribers > 0 else 0,
                "created_at": update.created_at.strftime("%b %d %Y %H:%M:%S"),
                "view_url": reverse("app.web.admin.incident_update.view", kwargs={'incident_id': incident_id, "update_id": update.id}),
                "edit_url": reverse("app.web.admin.incident_update.edit", kwargs={'incident_id': incident_id, "update_id": update.id}),
                "delete_url": reverse("app.api.private.v1.admin.incident_update.endpoint", kwargs={'incident_id': incident_id, "update_id": update.id})
            })

        return updates_list


class Incident_Update(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __incident_update = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__incident_update = Incident_Update_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def post(self, request, incident_id, update_id):

        self.__request.set_request(request)

        request_data = self.__request.get_request_data("post", {
            "status": "",
            "notify_subscribers": "",
            "message": "",
            "datetime": "",
        })

        self.__form.add_inputs({
            'message': {
                'value': request_data["message"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {}
            },
            'datetime': {
                'value': request_data["datetime"],
                'sanitize': {
                    'strip': {}
                },
                'validate': {}
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

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_private_failure(self.__form.get_errors(with_type=True)))

        result = self.__incident_update.update_one_by_id(update_id, {
            "notify_subscribers": self.__form.get_input_value("notify_subscribers"),
            "datetime": DateTimeField().clean(self.__form.get_input_value("datetime")),
            "message": self.__form.get_input_value("message"),
            "status": self.__form.get_input_value("status")
        })

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Incident update updated successfully.")
            }]))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while updating update.")
            }]))

    def delete(self, request, incident_id, update_id):

        self.__user_id = request.user.id

        if self.__incident_update.delete_one_by_id(update_id):
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Incident update deleted successfully.")
            }]))

        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while deleting incident update.")
            }]))


class Incident_Updates_Notify(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __incident_update = None
    __task = None
    __notification = None
    __subscriber = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__incident_update = Incident_Update_Module()
        self.__task = Task_Module()
        self.__notification = Notification_Module()
        self.__subscriber = Subscriber_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def post(self, request, incident_id, update_id):

        self.__user_id = request.user.id

        task = self.__task.delay("incident_update", {
            "incident_update_id": update_id
        }, self.__user_id)

        if task:
            self.__notification.create_notification({
                "highlight": "Incident Update",
                "notification": "notifying subscribers with the incident update",
                "url": "#",
                "type": Notification_Module.PENDING,
                "delivered": False,
                "user_id": self.__user_id,
                "task_id": task.id
            })


class Incident_Updates_Components(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __incident_update = None
    __task = None
    __notification = None
    __subscriber = None
    __incident_update_component = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__incident_update = Incident_Update_Module()
        self.__task = Task_Module()
        self.__notification = Notification_Module()
        self.__subscriber = Subscriber_Module()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__incident_update_component = Incident_Update_Component_Module()

    def post(self, request, incident_id, update_id):
        self.__user_id = request.user.id

        request_data = self.__request.get_request_data("post", {
            "type": "",
            "component_id": ""
        })

        self.__form.add_inputs({
            'component_id': {
                'value': request_data["component_id"],
                'sanitize': {},
                'validate': {}
            },
            'type': {
                'value': request_data["type"],
                'validate': {
                    'any_of': {
                        'param': [["operational", "degraded_performance", "partial_outage", "major_outage", "maintenance"]],
                        'error': _('Error! Type is invalid.')
                    }
                }
            }
        })

        self.__form.process()

        if not self.__form.is_passed():
            return JsonResponse(self.__response.send_private_failure(self.__form.get_errors(with_type=True)))

        result = self.__incident_update_component.insert_one({
            "component_id": self.__form.get_input_value("component_id"),
            "type": self.__form.get_input_value("type"),
            "incident_update_id": update_id
        })

        if result:
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Affected component created successfully.")
            }]))
        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while creating affected component.")
            }]))


class Incident_Updates_Component(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __incident_update_component = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__incident_update_component = Incident_Update_Component_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def delete(self, request, incident_id, update_id, item_id):
        self.__user_id = request.user.id

        if self.__incident_update_component.delete_one_by_id(item_id):
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Affected component deleted successfully.")
            }]))

        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while deleting affected component.")
            }]))
