"""
Incident Update Notification Module
"""

import datetime

from django.db.models.aggregates import Count
from django.utils import timezone

from app.models import Subscriber
from app.models import Incident_Update
from app.models import Incident_Update_Notification


class Incident_Update_Notification_Entity():

    def insert_one(self, item):
        new_item = Incident_Update_Notification()

        if "status" in item:
            new_item.status = item["status"]

        if "incident_update_id" in item:
            new_item.incident_update = None if item["incident_update_id"] is None else Incident_Update.objects.get(pk=item["incident_update_id"])

        if "subscriber_id" in item:
            new_item.subscriber = None if item["subscriber_id"] is None else Subscriber.objects.get(pk=item["subscriber_id"])

        new_item.save()
        return False if new_item.pk is None else new_item

    def update_one_by_id(self, id, data):
        item = self.get_one_by_id(id)
        if item is not False:

            if "status" in data:
                item.status = data["status"]

            if "incident_update_id" in data:
                item.incident_update = None if data["incident_update_id"] is None else Incident_Update.objects.get(pk=data["incident_update_id"])

            if "subscriber_id" in data:
                item.subscriber = None if data["subscriber_id"] is None else Subscriber.objects.get(pk=data["subscriber_id"])

            item.save()
            return True
        return False

    def is_subscriber_notified(self, incident_update_id, subscriber_id):
        try:
            notification = Incident_Update_Notification.objects.get(
                incident_update_id=incident_update_id,
                subscriber_id=subscriber_id
            )
            return False if notification.pk is None else notification
        except Exception:
            return False

    def get_one_by_id(self, id):
        try:
            item = Incident_Update_Notification.objects.get(id=id)
            return False if item.pk is None else item
        except Exception:
            return False

    def delete_one_by_id(self, id):
        item = self.get_one_by_id(id)
        if item is not False:
            count, deleted = item.delete()
            return True if count > 0 else False
        return False

    def count_by_status(self, status):
        return Incident_Update_Notification.objects.filter(status=status).count()

    def count_over_days(self, status, days=7):
        last_x_days = timezone.now() - datetime.timedelta(days)
        return Incident_Update_Notification.objects.filter(
            created_at__gte=last_x_days,
            status=status
        ).extra({"day": "date(created_at)"}).values("day").order_by('-day').annotate(count=Count("id"))
