"""
Incident Module
"""

# local Django
from app.modules.util.helpers import Helpers
from app.modules.entity.incident_update_entity import Incident_Update_Entity
from app.modules.entity.incident_entity import Incident_Entity
from app.modules.entity.incident_update_component_entity import Incident_Update_Component
from app.modules.entity.incident_update_notification_entity import Incident_Update_Notification


class Incident():

    __incident_update_entity = None
    __incident_entity = None
    __incident_update_component_entity = None
    __incident_update_notification_entity = None
    __helpers = None
    __logger = None

    def __init__(self):
        self.__incident_update_entity = Incident_Update_Entity()
        self.__incident_entity = Incident_Entity()
        self.__incident_update_component_entity = Incident_Update_Component()
        self.__incident_update_notification_entity = Incident_Update_Notification()
        self.__helpers = Helpers()
        self.__logger = self.__helpers.get_logger(__name__)

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

    def get_one_by_uri(self, uri):
        return {
            "headline": "Facebook Integration Issue",
            "headline_class": "text-danger",
            "sub_headline": "Incident Report for Silverback",
            "affected_components": ", ".join(["Cloud API", "Bmp API"]),
            "updates": [
                {
                    "type": "Resolved",
                    "body": "we began to see interruptions to Facebook integrations",
                    "date": "Feb 01, 2019 - 22:43 UTC"
                }
            ]
        }

    def get_many_for_period(self, period):
        return {
            "period": "May 2019 - July 2019",
            "incidents": [
                {
                    "date": "March 2019",
                    "incidents": [
                        {
                            "uri": "123",
                            "subject": "Partial network outage at one of our network suppliers",
                            "class": "text-danger",
                            "final_update": "This incident has been resolved.",
                            "period": "March 7, 08:56 CET - March 8, 2:56 CET"
                        },
                        {
                            "uri": "123",
                            "subject": "Partial network outage at one of our network suppliers",
                            "class": "text-danger",
                            "final_update": "This incident has been resolved.",
                            "period": "March 7, 08:56 CET - March 8, 2:56 CET"
                        },
                    ]
                },
                {
                    "date": "February 2019",
                    "incidents": []
                },
                {
                    "date": "January 2019",
                    "incidents": []
                }
            ]
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
