"""
Incident Entity Module
"""

import datetime

from django.db.models.aggregates import Count
from django.utils import timezone

from app.models import Incident


class Incident_Entity():

    def insert_one(self, incident):

        new_incident = Incident()

        if "name" in incident:
            new_incident.name = incident["name"]

        if "uri" in incident:
            new_incident.uri = incident["uri"]

        if "status" in incident:
            new_incident.status = incident["status"]

        new_incident.save()
        return False if new_incident.pk is None else new_incident

    def update_one_by_id(self, id, incident_data):
        incident = self.get_one_by_id(id)

        if incident is not False:
            if "name" in incident_data:
                incident.name = incident_data["name"]

            if "uri" in incident_data:
                incident.uri = incident_data["uri"]

            if "status" in incident_data:
                incident.status = incident_data["status"]

            incident.save()
            return True
        return False

    def count_all(self):
        return Incident.objects.count()

    def get_all(self, offset=None, limit=None):
        if offset is None or limit is None:
            return Incident.objects.order_by('-created_at').get()

        return Incident.objects.order_by('-created_at')[offset:limit+offset]

    def get_by_status(self, status):
        return Incident.objects.filter(status=status).order_by('-created_at')

    def get_one_by_id(self, incident_id):
        try:
            incident = Incident.objects.get(id=incident_id)
            return False if incident.pk is None else incident
        except Exception:
            return False

    def get_one_by_uri(self, uri):
        try:
            incident = Incident.objects.get(uri=uri)
            return False if incident.pk is None else incident
        except Exception:
            return False

    def delete_one_by_id(self, id):
        incident = self.get_one_by_id(id)
        if incident is not False:
            count, deleted = incident.delete()
            return True if count > 0 else False
        return False

    def count_over_days(self, days=7):
        last_x_days = timezone.now() - datetime.timedelta(days)
        return Incident.objects.filter(
            created_at__gte=last_x_days
        ).extra({"day": "date(created_at)"}).values("day").order_by('-day').annotate(count=Count("id"))
