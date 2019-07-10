"""
Notifications API Endpoint
"""

# Third Party Library
from django.views import View
from django.http import JsonResponse

# Local Library
from pyvalitron.form import Form
from app.modules.util.helpers import Helpers
from app.modules.core.request import Request
from app.modules.util.humanize import Humanize
from app.modules.core.response import Response
from app.modules.validation.extension import ExtraRules
from app.modules.core.notification import Notification as NotificationModule


class LatestNotifications(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __notification = None
    __correlation_id = None

    def __init__(self):
        self.__helpers = Helpers()
        self.__form = Form()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__response = Response()
        self.__request = Request()
        self.__notification = NotificationModule()
        self.__form.add_validator(ExtraRules())

    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__user_id = request.user.id

        return JsonResponse(self.__response.send_private_success(
            [],
            self.__notification.user_latest_notifications(self.__user_id),
            self.__correlation_id
        ))

    def post(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__user_id = request.user.id
        self.__request.set_request(request)

        request_data = self.__request.get_request_data("post", {
            "notification_id": ""
        })

        try:
            notification_id = int(request_data["notification_id"])
        except Exception:
            return JsonResponse(self.__response.send_private_success([], {}, self.__correlation_id))

        self.__notification.mark_notification(self.__user_id, notification_id)

        return JsonResponse(self.__response.send_private_success([], {}, self.__correlation_id))


class Notifications(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __notification = None
    __humanize = None
    __correlation_id = None

    def __init__(self):
        self.__helpers = Helpers()
        self.__form = Form()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__response = Response()
        self.__request = Request()
        self.__notification = NotificationModule()
        self.__humanize = Humanize()
        self.__form.add_validator(ExtraRules())

    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__user_id = request.user.id
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
            'notifications': self.__format_notification(self.__notification.get(self.__user_id, offset, limit)),
            'metadata': {
                'offset': offset,
                'limit': limit,
                'count': self.__notification.count(self.__user_id)
            }
        }, self.__correlation_id))

    def __format_notification(self, notifications):
        notifications_list = []

        for notification in notifications:
            notifications_list.append({
                "id": notification.id,
                "type": notification.type,
                "highlight": notification.highlight,
                "description": notification.notification,
                "url": notification.url,
                "delivered": notification.delivered,
                "created_at": self.__humanize.datetime(notification.created_at)
            })

        return notifications_list
