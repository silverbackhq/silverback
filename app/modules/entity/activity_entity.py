"""
Activity Entity Module
"""

from django.contrib.auth.models import User
from app.models import Activity


class Activity_Entity():

    def insert_one(self, activity):

        new_activity = Activity()

        if "activity" in activity:
            new_activity.activity = activity["activity"]

        if "user_id" in activity:
            new_activity.user = User.objects.get(pk=activity["user_id"])

        new_activity.save()
        return False if new_activity.pk is None else new_activity

    def update_one_by_id(self, id, activity_data):
        activity = self.get_one_by_id(id)

        if activity is not False:
            if "activity" in activity_data:
                activity.activity = activity_data["activity"]

            if "user_id" in activity_data:
                activity.user = User.objects.get(pk=activity_data["user_id"])

            activity.save()
            return True
        return False

    def count_all(self):
        return Activity.objects.count()

    def get_all(self, offset=None, limit=None):
        if offset is None or limit is None:
            return Activity.objects.order_by('-created_at').get()

        return Activity.objects.order_by('-created_at')[offset:limit+offset]

    def get_one_by_id(self, incident_id):
        try:
            activity = Activity.objects.get(id=incident_id)
            return False if activity.pk is None else activity
        except Exception:
            return False

    def delete_one_by_id(self, id):
        activity = self.get_one_by_id(id)
        if activity is not False:
            count, deleted = activity.delete()
            return True if count > 0 else False
        return False
