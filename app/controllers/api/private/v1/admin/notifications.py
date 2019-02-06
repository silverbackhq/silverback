"""
Notifications API Endpoint
"""

# Django
from django.views import View
from django.http import JsonResponse

# local Django
from app.modules.validation.form import Form
from app.modules.util.helpers import Helpers
from app.modules.util.humanize import Humanize
from app.modules.core.request import Request
from app.modules.core.response import Response
from app.modules.core.notification import Notification as Notification_Module


class LatestNotifications(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __notification = None

    def __init__(self):
        self.__helpers = Helpers()
        self.__form = Form()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__response = Response()
        self.__request = Request()
        self.__notification = Notification_Module()

    def get(self, request):
        self.__user_id = request.user.id

        return JsonResponse(self.__response.send_private_success(
            [],
            self.__notification.user_latest_notifications(self.__user_id)
        ))

    def post(self, request):

        self.__user_id = request.user.id

        self.__request.set_request(request)

        request_data = self.__request.get_request_data("post", {
            "notification_id": ""
        })

        try:
            notification_id = int(request_data["notification_id"])
        except Exception:
            return JsonResponse(self.__response.send_private_success([]))

        self.__notification.mark_notification(self.__user_id, notification_id)

        return JsonResponse(self.__response.send_private_success([]))


class Notifications(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __notification = None
    __humanize = None

    def __init__(self):
        self.__helpers = Helpers()
        self.__form = Form()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__response = Response()
        self.__request = Request()
        self.__notification = Notification_Module()
        self.__humanize = Humanize()

    def get(self, request):
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
        }))

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
