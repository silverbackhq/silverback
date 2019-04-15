"""
Incident Module
"""

from app.modules.entity.incident_update_entity import Incident_Update_Entity
from app.modules.entity.incident_entity import Incident_Entity
from app.modules.entity.incident_update_component_entity import Incident_Update_Component
from app.modules.entity.incident_update_notification_entity import Incident_Update_Notification


class Incident():

    __incident_update_entity = None
    __incident_entity = None
    __incident_update_component_entity = None
    __incident_update_notification_entity = None

    def __init__(self):
        self.__incident_update_entity = Incident_Update_Entity()
        self.__incident_entity = Incident_Entity()
        self.__incident_update_component_entity = Incident_Update_Component()
        self.__incident_update_notification_entity = Incident_Update_Notification()

    def get_one_by_id(self, id):
        incident = self.__incident_entity.get_one_by_id(id)

        if not incident:
            return False

        return {
            "id": incident.id,
            "name": incident.name,
            "uri": incident.uri,
            "status": incident.status
        }

    def generate_uri(self, size=6):

        uri = self.__helpers.random_generator(size)

        while self.__incident_entity.get_one_by_uri(uri):
            uri = self.__helpers.random_generator(size)

        return uri

    def insert_one(self, incident):
        return self.__incident_entity.insert_one(incident)

    def update_one_by_id(self, id, incident_data):
        return self.__incident_entity.update_one_by_id(id, incident_data)

    def count_all(self):
        return self.__incident_entity.count_all()

    def get_all(self, offset=None, limit=None):
        return self.__incident_entity.get_all(offset, limit)

    def delete_one_by_id(self, id):
        return self.__incident_entity.delete_one_by_id(id)
