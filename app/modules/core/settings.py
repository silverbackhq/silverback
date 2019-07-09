"""
Settings Module
"""

# Local Library
from app.modules.entity.option_entity import OptionEntity


class Settings():

    __option_entity = None

    def __init__(self):
        self.__option_entity = OptionEntity()

    def update_options(self, options):
        status = True
        for key, value in options.items():
            status &= self.__option_entity.update_value_by_key(key, value)
        return status

    def get_value_by_key(self, key, default=""):
        return self.__option_entity.get_value_by_key(key, default)
