"""
Notifications API Endpoint
"""

# Django
from django.views import View
from django.http import JsonResponse

# local Django
from app.modules.validation.form import Form
from app.modules.util.helpers import Helpers
from app.modules.core.request import Request
from app.modules.core.response import Response
from app.modules.core.notification import Notification as Notification_Module


class Notifications(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __notification_module = None

    def __init__(self):
        self.__helpers = Helpers()
        self.__form = Form()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__response = Response()
        self.__request = Request()
        self.__notification_module = Notification_Module()

    def get(self, request):
        self.__user_id = request.user.id
        return JsonResponse(self.__response.send_private_success(
            [],
            self.__notification_module.user_latest_notifications(self.__user_id)
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

        self.__notification_module.mark_notification(self.__user_id, notification_id)

        return JsonResponse(self.__response.send_private_success([]))
