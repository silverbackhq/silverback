"""
Incident Update Entity Module
"""

import datetime

from django.db.models.aggregates import Count
from django.utils import timezone

from app.models import Incident
from app.models import Incident_Update


class Incident_Update_Entity():

    def insert_one(self, update):

        new_update = Incident_Update()

        if "status" in update:
            new_update.status = update["status"]

        if "notify_subscribers" in update:
            new_update.notify_subscribers = update["notify_subscribers"]

        if "total_suscribers" in update:
            new_update.total_suscribers = update["total_suscribers"]

        if "notified_subscribers" in update:
            new_update.notified_subscribers = update["notified_subscribers"]

        if "failed_subscribers" in update:
            new_update.failed_subscribers = update["failed_subscribers"]

        if "datetime" in update:
            new_update.datetime = update["datetime"]

        if "message" in update:
            new_update.message = update["message"]

        if "incident_id" in update:
            new_update.incident = None if update["incident_id"] is None else Incident.objects.get(pk=update["incident_id"])

        new_update.save()
        return False if new_update.pk is None else new_update

    def update_one_by_id(self, id, update_data):
        update = self.get_one_by_id(id)
        if update is not False:

            if "status" in update_data:
                update.status = update_data["status"]

            if "notify_subscribers" in update_data:
                update.notify_subscribers = update_data["notify_subscribers"]

            if "total_suscribers" in update_data:
                update.total_suscribers = update_data["total_suscribers"]

            if "notified_subscribers" in update_data:
                update.notified_subscribers = update_data["notified_subscribers"]

            if "failed_subscribers" in update_data:
                update.failed_subscribers = update_data["failed_subscribers"]

            if "datetime" in update_data:
                update.datetime = update_data["datetime"]

            if "message" in update_data:
                update.message = update_data["message"]

            if "incident_id" in update_data:
                update.incident = None if update_data["incident_id"] is None else Incident.objects.get(pk=update_data["incident_id"])

            update.save()

            return True
        return False

    def count_all(self, incident_id):
        return Incident_Update.objects.filter(incident_id=incident_id).count()

    def get_all(self, incident_id, offset=None, limit=None):
        if offset is None or limit is None:
            return Incident_Update.objects.filter(incident_id=incident_id).order_by('-created_at').get()

        return Incident_Update.objects.filter(incident_id=incident_id).order_by('-created_at')[offset:limit+offset]

    def get_one_by_id(self, update_id):
        try:
            incident_update = Incident_Update.objects.get(id=update_id)
            return False if incident_update.pk is None else incident_update
        except Exception:
            return False

    def delete_one_by_id(self, id):
        incident_update = self.get_one_by_id(id)
        if incident_update is not False:
            count, deleted = incident_update.delete()
            return True if count > 0 else False
        return False

    def count_over_days(self, days=7):
        last_x_days = timezone.now() - datetime.timedelta(days)
        return Incident_Update.objects.filter(
            created_at__gte=last_x_days
        ).extra({"day": "date(created_at)"}).values("day").order_by('-day').annotate(count=Count("id"))
