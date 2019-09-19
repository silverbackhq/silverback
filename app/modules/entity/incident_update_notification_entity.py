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

# Standard Library
import datetime

# Third Party Library
from django.utils import timezone
from django.db.models.aggregates import Count

# Local Library
from app.models import Subscriber
from app.models import IncidentUpdate
from app.models import IncidentUpdateNotification


class IncidentUpdateNotificationEntity():

    def insert_one(self, item):
        new_item = IncidentUpdateNotification()

        if "status" in item:
            new_item.status = item["status"]

        if "incident_update_id" in item:
            new_item.incident_update = None if item["incident_update_id"] is None else IncidentUpdate.objects.get(pk=item["incident_update_id"])

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
                item.incident_update = None if data["incident_update_id"] is None else IncidentUpdate.objects.get(pk=data["incident_update_id"])

            if "subscriber_id" in data:
                item.subscriber = None if data["subscriber_id"] is None else Subscriber.objects.get(pk=data["subscriber_id"])

            item.save()
            return True
        return False

    def is_subscriber_notified(self, incident_update_id, subscriber_id):
        try:
            notification = IncidentUpdateNotification.objects.get(
                incident_update_id=incident_update_id,
                subscriber_id=subscriber_id
            )
            return False if notification.pk is None else notification
        except Exception:
            return False

    def count_by_update_status(self, update_id, status):
        return IncidentUpdateNotification.objects.filter(status=status, incident_update_id=update_id).count()

    def get_one_by_id(self, id):
        try:
            item = IncidentUpdateNotification.objects.get(id=id)
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
        return IncidentUpdateNotification.objects.filter(status=status).count()

    def count_over_days(self, status, days=7):
        last_x_days = timezone.now() - datetime.timedelta(days)
        return IncidentUpdateNotification.objects.filter(
            created_at__gte=last_x_days,
            status=status
        ).extra({"day": "date(created_at)"}).values("day").order_by('-day').annotate(count=Count("id"))
