"""
Correlation Middleware
"""

# Local Library
from app.modules.util.helpers import Helpers


class Correlation():

    __helpers = None

    def __init__(self, get_response):
        self.__helpers = Helpers()
        self.get_response = get_response

    def __call__(self, request):
        request.META["X-Correlation-ID"] = self.__helpers.generate_uuid()

        response = self.get_response(request)

        return response
