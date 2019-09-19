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
from app.modules.entity.incident_update_component_entity import IncidentUpdateComponentEntity


class IncidentUpdateComponent():

    __incident_update_component_entity = None

    def __init__(self):
        self.__incident_update_component_entity = IncidentUpdateComponentEntity()

    def get_one_by_id(self, id):
        item = self.__incident_update_component_entity.get_one_by_id(id)

        if not item:
            return False

        return {
            "id": item.id,
            "incident_update": item.incident_update,
            "component": item.component,
            "type": item.type
        }

    def insert_one(self, item):
        return self.__incident_update_component_entity.insert_one(item)

    def update_one_by_id(self, id, item_data):
        return self.__incident_update_component_entity.update_one_by_id(id, item_data)

    def count_all(self, update_id):
        return self.__incident_update_component_entity.count_all(update_id)

    def get_all(self, update_id):
        return self.__incident_update_component_entity.get_all(update_id)

    def delete_one_by_id(self, id):
        return self.__incident_update_component_entity.delete_one_by_id(id)
