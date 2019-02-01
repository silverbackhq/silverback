"""
Activity Module
"""

# local Django
from app.modules.util.helpers import Helpers
from app.modules.entity.activity_entity import Activity_Entity


class Activity():

    __activity_entity = None
    __helpers = None
    __logger = None

    def __init__(self):
        self.__activity_entity = Activity_Entity()
        self.__helpers = Helpers()
        self.__logger = self.__helpers.get_logger(__name__)

    def get_one_by_id(self, id):
        activity = self.__activity_entity.get_one_by_id(id)

        if not activity:
            return False

        return {
            "id": activity.id,
            "activity": activity.activity,
            "user": activity.user
        }

    def track(self, user_id, activity):
        return self.__activity_entity.insert_one({
            "activity": activity,
            "user_id": user_id
        })

    def insert_one(self, activity):
        return self.__activity_entity.insert_one(activity)

    def update_one_by_id(self, id, activity_data):
        return self.__activity_entity.update_one_by_id(id, activity_data)

    def count(self, user_id):
        return self.__activity_entity.count(user_id)

    def count_all(self):
        return self.__activity_entity.count_all()

    def get(self, user_id, offset=None, limit=None):
        return self.__activity_entity.get(user_id, offset, limit)

    def get_all(self, offset=None, limit=None):
        return self.__activity_entity.get_all(offset, limit)

    def delete_one_by_id(self, id):
        return self.__activity_entity.delete_one_by_id(id)
