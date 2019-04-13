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
        correlation_id = request.META["X-Correlation-ID"]

        self.__logger.debug(_("Request Method: %(method)s {'correlationId':'%(correlationId)s'}") % {
            "method": request.method,
            "correlationId": correlation_id
        })
        self.__logger.debug(_("Request URL: %(path)s {'correlationId':'%(correlationId)s'}") % {
            "path": request.path,
            "correlationId": correlation_id
        })
        self.__logger.debug(_("Request Body: %(body)s {'correlationId':'%(correlationId)s'}") % {
            "body": request.body,
            "correlationId": correlation_id
        })

        response = self.get_response(request)

        return response
