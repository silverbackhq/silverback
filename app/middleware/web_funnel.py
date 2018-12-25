"""
Logging Middleware
"""

# local Django
from app.modules.util.helpers import Helpers
from app.modules.core.funnel import Funnel


class Web_Funnel():

    __helpers = None
    __logger = None
    __funnel = None
    __roles = {

    }

    def __init__(self, get_response):
        self.__helpers = Helpers()
        self.__funnel = Funnel()
        self.get_response = get_response
        self.__logger = self.__helpers.get_logger(__name__)

    def __call__(self, request):

        self.__funnel.set_rules(self.__roles)
        self.__funnel.set_request(request)

        if self.__funnel.action_needed():
            return self.__funnel.fire()

        response = self.get_response(request)

        return response
