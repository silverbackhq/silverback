"""
    Request Module
    ~~~~~~~~~~~~~~

    :copyright: silverbackhq
    :license: BSD-3-Clause
"""

# Third Party Library
from django.utils.translation import gettext as _

# Local Library
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
        log_data = {}
        correlation_id = self.__request.META["X-Correlation-ID"] if "X-Correlation-ID" in self.__request.META else ""
        data_bag = self.__request.POST if method.lower() == "post" else self.__request.GET

        for key, default in predicted.items():
            if "password" in key:
                log_data[key] = "<hidden>" if key in data_bag else default
            elif "token" in key:
                log_data[key] = "<hidden>" if key in data_bag else default
            else:
                log_data[key] = data_bag[key] if key in data_bag else default
            request_data[key] = data_bag[key] if key in data_bag else default

        self.__logger.debug(_("App Incoming Request: %(data)s {'correlationId':'%(correlationId)s'}") % {
            "data": self.__helpers.json_dumps(log_data),
            "correlationId": correlation_id
        })

        return request_data
