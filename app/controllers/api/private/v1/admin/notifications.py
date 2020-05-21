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

# Local Library
from app.modules.util.humanize import Humanize
from app.controllers.controller import Controller
from app.modules.core.decorators import allow_if_authenticated
from app.modules.core.notification import Notification as NotificationModule


class LatestNotifications(View, Controller):
    """List and Update Latest Notifications Private Endpoint Controller"""

    def __init__(self):
        self.__notification = NotificationModule()

    @allow_if_authenticated
    def get(self, request):

        self.__correlation_id = self.get_correlation(request)
        self.__user_id = request.user.id

        return self.json(
            [],
            self.__notification.user_latest_notifications(self.__user_id)
        )

    @allow_if_authenticated
    def post(self, request):

        self.__correlation_id = self.get_correlation(request)
        self.__user_id = request.user.id
        self.get_request().set_request(request)

        request_data = self.get_request().get_request_data("post", {
            "notification_id": ""
        })

        try:
            notification_id = int(request_data["notification_id"])
        except Exception:
            return self.json([])

        self.__notification.mark_notification(self.__user_id, notification_id)

        return self.json([])


class Notifications(View, Controller):
    """List Notifications Private Endpoint Controller"""

    def __init__(self):
        self.__notification = NotificationModule()
        self.__humanize = Humanize()

    @allow_if_authenticated
    def get(self, request):

        self.__correlation_id = self.get_correlation(request)
        self.__user_id = request.user.id
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
            'notifications': self.__format_notification(self.__notification.get(self.__user_id, offset, limit)),
            'metadata': {
                'offset': offset,
                'limit': limit,
                'count': self.__notification.count(self.__user_id)
            }
        })

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
