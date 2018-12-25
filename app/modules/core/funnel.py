"""
Funnel Module
"""

# local Django
from app.modules.util.helpers import Helpers


class Funnel():

    __helpers = None
    __logger = None
    __rules = {}
    __request = {}

    def __init__(self):
        self.__helpers = Helpers()
        self.__logger = self.__helpers.get_logger(__name__)

    def set_rules(self, rules):
        self.__rules = rules

    def set_request(self, request):
        self.__request = request

    def action_needed(self):
        return False

    def fire(self):
        pass

    def _parse(self):
        # __route_name = request.resolver_match.url_name
        # if request.user and request.user.is_authenticated:
        #    self.__is_auth = True
        #    self.__user_id = request.user.id
        #    self.__username = request.user
        pass
