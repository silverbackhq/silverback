"""
Task Module
"""

# Local Library
from app.modules.util.humanize import Humanize
from app.modules.entity.option_entity import Option_Entity
from app.modules.entity.notification_entity import Notification_Entity


class Notification():

    PENDING = "pending"
    FAILED = "failed"
    PASSED = "passed"
    ERROR = "error"
    MESSAGE = "message"

    __notification_entity = None
    __option_entity = None
    __humanize = None
    __app_name = None

    def __init__(self):
        self.__notification_entity = Notification_Entity()
        self.__option_entity = Option_Entity()
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
