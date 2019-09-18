"""
    Errors Middleware
    ~~~~~~~~~~~~~~

    :copyright: silverbackhq
    :license: BSD-3-Clause
"""

# Third Party Library
from django.http import JsonResponse
from django.utils.translation import gettext as _

# Local Library
from app.modules.util.helpers import Helpers
from app.modules.core.response import Response


class Errors():

    __helpers = None
    __logger = None

    def __init__(self, get_response):
        self.__helpers = Helpers()
        self.get_response = get_response
        self.__logger = self.__helpers.get_logger(__name__)

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):

        correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""

        self.__logger.error(
            _("The server encountered something unexpected! %(method)s:%(path)s  - %(name)s - %(exception)s {'correlationId':'%(correlationId)s'}") % {
                "method": request.method,
                "path": request.path,
                "name": exception.__class__.__name__,
                "exception": exception,
                "correlationId": correlation_id
            }
        )

        self.__logger.exception(exception)

        if request.is_ajax():
            response = Response()
            return JsonResponse(response.send_private_failure([{
                "type": "error",
                "message": _("Something goes wrong! Please contact a system administrator.")
            }], {}, correlation_id))

        return None
