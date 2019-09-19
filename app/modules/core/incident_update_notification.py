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
from app.modules.entity.incident_update_notification_entity import IncidentUpdateNotificationEntity


class IncidentUpdateNotification():

    PENDING = "pending"
    FAILED = "failed"
    SUCCESS = "success"

    def __init__(self):
        self.__incident_update_notification_entity = IncidentUpdateNotificationEntity()

    def get_one_by_id(self, id):
        item = self.__incident_update_notification_entity.get_one_by_id(id)

        if not item:
            return False

        return {
            "id": item.id,
            "incident_update": item.incident_update,
            "subscriber": item.subscriber,
            "status": item.status
        }

    def count_by_update_status(self, update_id, status):
        return self.__incident_update_notification_entity.count_by_update_status(update_id, status)

    def insert_one(self, item):
        return self.__incident_update_notification_entity.insert_one(item)

    def update_one_by_id(self, id, data):
        return self.__incident_update_notification_entity.update_one_by_id(id, data)

    def is_subscriber_notified(self, incident_update_id, subscriber_id):
        return self.__incident_update_notification_entity.is_subscriber_notified(incident_update_id, subscriber_id)

    def delete_one_by_id(self, id):
        return self.__incident_update_notification_entity.delete_one_by_id(id)
