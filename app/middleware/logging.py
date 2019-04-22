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
        correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""

        self.__logger.debug(_("Request Method: %(method)s {'correlationId':'%(correlationId)s'}") % {
            "method": request.method,
            "correlationId": correlation_id
        })
        self.__logger.debug(_("Request URL: %(path)s {'correlationId':'%(correlationId)s'}") % {
            "path": request.path,
            "correlationId": correlation_id
        })
        self.__logger.debug(_("Request Body: %(body)s {'correlationId':'%(correlationId)s'}") % {
            "body": self.__hide_secure_values(request.body),
            "correlationId": correlation_id
        })

        response = self.get_response(request)

        return response

    def __hide_secure_values(self, request_body):
        filtered_body = []
        request_body = str(request_body)
        if len(request_body) == 0:
            return "&".join(filtered_body)

        if "&" in request_body:
            request_body = request_body.split("&")
            for item in request_body:
                if "=" in item:
                    item = item.split("=")
                    if "password" in item[0]:
                        item[1] = "<hidden>"
                    if "token" in item[0]:
                        item[1] = "<hidden>"
                    filtered_body.append("%s=%s" % (item[0], item[1]))

        return "&".join(filtered_body)
