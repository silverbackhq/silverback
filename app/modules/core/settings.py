"""
Settings Module
"""

# local Django
from app.modules.util.helpers import Helpers
from app.modules.entity.option_entity import Option_Entity


class Settings():

    __option_entity = None
    __helpers = None
    __logger = None

    def __init__(self):
        self.__option_entity = Option_Entity()
        self.__helpers = Helpers()
        self.__logger = self.__helpers.get_logger(__name__)

    def update_options(self, options):
        status = True
        for key, value in options.items():
            status &= self.__option_entity.update_value_by_key(key, value)
        return status
