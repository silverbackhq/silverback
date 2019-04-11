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
        self.__logger.debug(_("Request Method: %(method) {'correlationId':'%(correlationId)'}") % ({
            "method": request.method,
            "correlationId": request.META["X-Correlation-ID"]
        }))
        self.__logger.debug(_("Request URL: %(path) {'correlationId':'%(correlationId)'}") % ({
            "path": request.path,
            "correlationId": request.META["X-Correlation-ID"]
        }))
        self.__logger.debug(_("Request Body: %(body) {'correlationId':'%(correlationId)'}") % ({
            "body": request.body,
            "correlationId": request.META["X-Correlation-ID"]
        }))

        response = self.get_response(request)

        return response
