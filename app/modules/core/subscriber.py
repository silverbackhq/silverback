"""
Subscriber Module
"""

# local Django
from app.modules.util.helpers import Helpers
from app.modules.entity.subscriber_entity import Subscriber_Entity


class Subscriber():

    __subscriber_entity = None
    __helpers = None
    __logger = None

    def __init__(self):
        self.__helpers = Helpers()
        self.__subscriber_entity = Subscriber_Entity()
        self.__logger = self.__helpers.get_logger(__name__)

    def get_one_by_id(self, id):
        subscriber = self.__subscriber_entity.get_one_by_id(id)

        if not subscriber:
            return False

        return {
            "id": subscriber.id,
            "email": subscriber.email,
            "phone": subscriber.phone,
            "endpoint": subscriber.endpoint,
            "auth_token": subscriber.auth_token,
            "type": subscriber.type,
            "status": subscriber.status,
            "external_id": subscriber.external_id
        }

    def insert_one(self, subscriber):
        return self.__subscriber_entity.insert_one(subscriber)

    def update_one_by_id(self, id, subscriber_data):
        return self.__subscriber_entity.update_one_by_id(id, subscriber_data)

    def count_all(self):
        return self.__subscriber_entity.count_all()

    def get_all(self, offset=None, limit=None):
        return self.__subscriber_entity.get_all(offset, limit)

    def delete_one_by_id(self, id):
        return self.__subscriber_entity.delete_one_by_id(id)
