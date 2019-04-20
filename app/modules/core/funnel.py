"""
Funnel Module
"""


class Funnel():

    __rules = {}
    __request = {}

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
