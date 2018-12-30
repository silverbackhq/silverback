"""
Activity Module
"""

# local Django
from app.modules.util.helpers import Helpers


class Activity():

    __helpers = None
    __logger = None

    def __init__(self):
        self.__helpers = Helpers()
        self.__logger = self.__helpers.get_logger(__name__)
