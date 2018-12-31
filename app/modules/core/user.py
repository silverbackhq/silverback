"""
User Module
"""

# local Django
from app.modules.util.helpers import Helpers
from app.modules.entity.user_entity import User_Entity


class User():

    __helpers = None
    __logger = None
    __user_entity = None

    def __init__(self):
        self.__helpers = Helpers()
        self.__logger = self.__helpers.get_logger(__name__)
        self.__user_entity = User_Entity()

    def count_all(self):
        return self.__user_entity.count_all()

    def get_all(self, offset=None, limit=None):
        return self.__user_entity.get_all(offset, limit)

    def delete_one_by_id(self, id):
        return self.__user_entity.delete_one_by_id(id)
