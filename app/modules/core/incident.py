"""
Incident Module
"""

# Local Library
from app.modules.util.helpers import Helpers
from app.modules.entity.incident_entity import IncidentEntity
from app.modules.entity.incident_update_entity import IncidentUpdateEntity
from app.modules.entity.incident_update_component_entity import IncidentUpdateComponent
from app.modules.entity.incident_update_notification_entity import IncidentUpdateNotification


class Incident():

    __incident_update_entity = None
    __incident_entity = None
    __incident_update_component_entity = None
    __incident_update_notification_entity = None
    __helpers = None

    def __init__(self):
        self.__incident_update_entity = IncidentUpdateEntity()
        self.__incident_entity = IncidentEntity()
        self.__incident_update_component_entity = IncidentUpdateComponent()
        self.__incident_update_notification_entity = IncidentUpdateNotification()
        self.__helpers = Helpers()

    def get_one_by_id(self, id):
        incident = self.__incident_entity.get_one_by_id(id)

        if not incident:
            return False

        return {
            "id": incident.id,
            "name": incident.name,
            "uri": incident.uri,
            "status": incident.status,
            "datetime": incident.datetime
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

    def get_incident_from_days(self, days=7):
        return self.__incident_entity.get_incident_from_days(days)
