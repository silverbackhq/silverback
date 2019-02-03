"""
Incident Update Component Module
"""

import datetime

from django.db.models.aggregates import Count
from django.utils import timezone

from app.models import Component
from app.models import Incident_Update
from app.models import Incident_Update_Component


class Incident_Update_Component_Entity():

    def insert_one(self, item):
        new_item = Incident_Update_Component()

        if "type" in item:
            new_item.type = item["type"]

        if "incident_update_id" in item:
            new_item.incident_update = None if item["incident_update_id"] is None else Incident_Update.objects.get(pk=item["incident_update_id"])

        if "component_id" in item:
            new_item.component = None if item["component_id"] is None else Component.objects.get(pk=item["component_id"])

        new_item.save()
        return False if new_item.pk is None else new_item

    def update_one_by_id(self, id, data):
        item = self.get_one_by_id(id)
        if item is not False:

            if "type" in data:
                item.type = data["type"]

            if "incident_update_id" in data:
                item.incident_update = None if data["incident_update_id"] is None else Incident_Update.objects.get(pk=data["incident_update_id"])

            if "component_id" in data:
                item.component = None if data["component_id"] is None else Component.objects.get(pk=data["component_id"])

            item.save()
            return True
        return False

    def count_all(self, incident_update_id):
        return Incident_Update_Component.objects.filter(incident_update_id=incident_update_id).count()

    def get_all(self, incident_update_id):
        return Incident_Update_Component.objects.filter(incident_update_id=incident_update_id).order_by('-created_at')

    def get_one_by_id(self, id):
        try:
            item = Incident_Update_Component.objects.get(id=id)
            return False if item.pk is None else item
        except Exception:
            return False

    def delete_one_by_id(self, id):
        item = self.get_one_by_id(id)
        if item is not False:
            count, deleted = item.delete()
            return True if count > 0 else False
        return False

    def count_over_days(self, days=7):
        last_x_days = timezone.now() - datetime.timedelta(days)
        return Incident_Update_Component.objects.filter(
            created_at__gte=last_x_days
        ).extra({"day": "date(created_at)"}).values("day").order_by('-day').annotate(count=Count("id"))
