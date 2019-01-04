"""
Incident Update Entity Module
"""

from app.models import Incident
from app.models import Incident_Update


class Incident_Update_Entity():

    def insert_one(self, update):

        new_update = Incident_Update()

        if "status" in update:
            new_update.status = update["status"]

        if "notify_subscribers" in update:
            new_update.notify_subscribers = update["notify_subscribers"]

        if "time" in update:
            new_update.time = update["time"]

        if "message" in update:
            new_update.message = update["message"]

        if "incident_id" in update:
            new_update.incident = None if update["incident_id"] is None else Incident.objects.get(pk=update["incident_id"])

        new_update.save()
        return False if new_update.pk is None else new_update

    def update_one_by_id(self, id, update_data):
        update = self.get_one_by_id(id)

        if update is not False:

            if "status" in update:
                update.status = update["status"]

            if "notify_subscribers" in update:
                update.notify_subscribers = update["notify_subscribers"]

            if "time" in update:
                update.time = update["time"]

            if "message" in update:
                update.message = update["message"]

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
