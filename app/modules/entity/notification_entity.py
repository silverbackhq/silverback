"""
Notification Entity Module
"""

# Third Party Library
from django.contrib.auth.models import User

# Local Library
from app.models import Task
from app.models import Notification


class Notification_Entity():

    def insert_one(self, notification):
        """Insert Notification"""
        notification = Notification(
            highlight=notification["highlight"],
            notification=notification["notification"],
            url=notification["url"],
            type=notification["type"],
            delivered=notification["delivered"],
            user=User.objects.get(pk=notification["user_id"]),
            task=Task.objects.get(pk=notification["task_id"]) if notification["task_id"] is not None else notification["task_id"]
        )

        notification.save()
        return False if notification.pk is None else notification

    def insert_many(self, notifications):
        """Insert Many Notifications"""
        status = True
        for notification in notifications:
            status &= True if self.insert_one(notification) is not False else False
        return status

    def get_one_by_id(self, id):
        """Get Notification By ID"""
        try:
            notification = Notification.objects.get(pk=id)
            return False if notification.pk is None else notification
        except Exception:
            return False

    def get_one_by_task_id(self, task_id):
        """Get Notification By Task ID"""
        try:
            notification = Notification.objects.get(task=task_id)
            return False if notification.pk is None else notification
        except Exception:
            return False

    def get_many_by_user(self, user_id, order_by, asc, count=5):
        """Get Many Notifications By User ID"""
        notifications = Notification.objects.filter(user=user_id).order_by(order_by if asc else "-%s" % order_by)[:count]
        return notifications

    def update_one_by_id(self, id, new_data):
        """Update Notification By ID"""
        notification = self.get_one_by_id(id)
        if notification is not False:

            if "highlight" in new_data:
                notification.highlight = new_data["highlight"]

            if "notification" in new_data:
                notification.notification = new_data["notification"]

            if "url" in new_data:
                notification.url = new_data["url"]

            if "type" in new_data:
                notification.type = new_data["type"]

            if "delivered" in new_data:
                notification.delivered = new_data["delivered"]

            if "user_id" in new_data:
                notification.user = User.objects.get(pk=new_data["user_id"])

            if "task_id" in new_data:
                notification.task = Task.objects.get(pk=notification["task_id"]) if notification["task_id"] is not None else notification["task_id"]

            notification.save()
            return True
        return False

    def update_one_by_task_id(self, task_id, new_data):
        notification = self.get_one_by_task_id(task_id)

        if notification is not False:

            if "highlight" in new_data:
                notification.highlight = new_data["highlight"]

            if "notification" in new_data:
                notification.notification = new_data["notification"]

            if "url" in new_data:
                notification.url = new_data["url"]

            if "type" in new_data:
                notification.type = new_data["type"]

            if "delivered" in new_data:
                notification.delivered = new_data["delivered"]

            if "created_at" in new_data:
                notification.created_at = new_data["created_at"]

            if "updated_at" in new_data:
                notification.updated_at = new_data["updated_at"]

            if "user_id" in new_data:
                notification.user = User.objects.get(pk=new_data["user_id"])

            if "task_id" in new_data:
                notification.task = Task.objects.get(pk=notification["task_id"]) if notification["task_id"] is not None else notification["task_id"]

            notification.save()
            return True
        return False

    def get_one_by_id_and_user(self, id, user_id):
        try:
            notification = Notification.objects.get(pk=id, user=user_id)
            return False if notification.pk is None else notification
        except Exception:
            return False

    def delete_one_by_id(self, id):
        """Delete Notification By ID"""
        notification = self.get_one_by_id(id)
        if notification is not False:
            count, deleted = notification.delete()
            return True if count > 0 else False
        return False

    def count(self, user_id=None):
        if user_id is None:
            return Notification.objects.count()
        else:
            return Notification.objects.filter(user_id=user_id).count()

    def get(self, user_id, offset=None, limit=None):
        if offset is None or limit is None:
            return Notification.objects.filter(user_id=user_id).order_by('-created_at')

        return Notification.objects.filter(user_id=user_id).order_by('-created_at')[offset:limit+offset]
