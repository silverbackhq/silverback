"""
Incident Update Component Module
"""

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
