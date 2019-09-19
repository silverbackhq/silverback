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

# Local Library
from app.modules.util.humanize import Humanize
from app.modules.entity.option_entity import OptionEntity
from app.modules.entity.notification_entity import NotificationEntity


class Notification():

    PENDING = "pending"
    FAILED = "failed"
    PASSED = "passed"
    ERROR = "error"
    MESSAGE = "message"

    def __init__(self):
        self.__notification_entity = NotificationEntity()
        self.__option_entity = OptionEntity()
        self.__humanize = Humanize()
        option = self.__option_entity.get_one_by_key("app_name")
        self.__app_name = option.value if option is not False else ""

    def create_notification(self, data):
        return self.__notification_entity.insert_one(data)

    def user_latest_notifications(self, user_id, count=5):

        notifications = self.__notification_entity.get_many_by_user(user_id, "created_at", False, count)

        result = {
            "notifications": [],
            "status": "read"
        }

        for notification in notifications:
            if not notification.delivered:
                result["status"] = "unread"

            result["notifications"].append({
                "id": notification.id,
                "type": notification.type,
                "highlight": notification.highlight,
                "description": notification.notification,
                "url": notification.url,
                "delivered": notification.delivered,
                "time": self.__humanize.datetime(notification.created_at)
            })

        return result

    def update_task_notification(self, task_id, type, delivered=False):
        return self.__notification_entity.update_one_by_task_id(task_id, {
            "type": type,
            "delivered": delivered
        })

    def mark_notification(self, user_id, notification_id):
        if self.__notification_entity.get_one_by_id_and_user(notification_id, user_id):
            return self.__notification_entity.update_one_by_id(notification_id, {"delivered": True})

        return False

    def get(self, user_id, offset=None, limit=None):
        return self.__notification_entity.get(user_id, offset, limit)

    def count(self, user_id=None):
        return self.__notification_entity.count(user_id)
