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
        pass
