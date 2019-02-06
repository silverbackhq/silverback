"""
Logging Middleware
"""

# Django
from django.utils.translation import gettext as _

# local Django
from app.modules.util.helpers import Helpers


class Logging():

    __helpers = None
    __logger = None

    def __init__(self, get_response):
        self.__helpers = Helpers()
        self.get_response = get_response
        self.__logger = self.__helpers.get_logger(__name__)

    def __call__(self, request):
        self.__logger.debug(_("Request Method: %s {'correlationId':'%s'}") % (request.method, request.META["X-Correlation-ID"]))
        self.__logger.debug(_("Request URL: %s {'correlationId':'%s'}") % (request.path, request.META["X-Correlation-ID"]))
        self.__logger.debug(_("Request Body: %s {'correlationId':'%s'}") % (request.body, request.META["X-Correlation-ID"]))

        response = self.get_response(request)

        return response
