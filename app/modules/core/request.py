"""
Request Module
"""

# Django
from django.utils.translation import gettext as _

# local Django
from app.modules.util.helpers import Helpers


class Request():

    __request = None
    __helpers = None
    __logger = None

    def __init__(self, request=None):
        self.__request = request
        self.__helpers = Helpers()
        self.__logger = self.__helpers.get_logger(__name__)

    def set_request(self, request):
        self.__request = request

    def get_request_data(self, method, predicted):
        request_data = {}
        data_bag = self.__request.POST if method.lower() == "post" else self.__request.GET

        for key, default in predicted.items():
            request_data[key] = data_bag[key] if key in data_bag else default

        self.__logger.debug(_("App Incoming Request: ") + self.__helpers.json_dumps(request_data))
        return request_data
