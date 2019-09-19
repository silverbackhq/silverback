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
from django.http import JsonResponse

# Local Library
from pyvalitron.form import Form
from app.modules.util.helpers import Helpers
from app.modules.core.request import Request
from app.modules.util.humanize import Humanize
from app.modules.core.response import Response
from app.modules.validation.extension import ExtraRules
from app.modules.core.decorators import allow_if_authenticated
from app.modules.core.notification import Notification as NotificationModule


class LatestNotifications(View):
    """List and Update Latest Notifications Private Endpoint Controller"""

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

    @allow_if_authenticated
    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__user_id = request.user.id

        return JsonResponse(self.__response.send_private_success(
            [],
            self.__notification.user_latest_notifications(self.__user_id),
            self.__correlation_id
        ))

    @allow_if_authenticated
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
    """List Notifications Private Endpoint Controller"""

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

    @allow_if_authenticated
    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__user_id = request.user.id
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
