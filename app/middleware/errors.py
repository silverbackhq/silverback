"""
Errors Middleware
"""

# Django
from django.utils.translation import gettext as _
from django.http import JsonResponse

# local Django
from app.modules.core.response import Response
from app.modules.util.helpers import Helpers


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
        self.__logger.error(
            _("The server encountered something unexpected! %s %s  - %s - %s") % (
                request.method,
                request.path,
                exception.__class__.__name__,
                exception
            )
        )

        if request.is_ajax():
            response = Response()
            return JsonResponse(response.send_private_failure([{
                "type": "error",
                "message": _("Something goes wrong! Please contact a system administrator.")
            }]))

        return None
