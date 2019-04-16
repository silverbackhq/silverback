"""
Login Web Controller
"""

from django.views import View
from django.http import JsonResponse
from app.modules.core.response import Response
from app.modules.core.health import Health


class HealthCheck(View):

    __response = None
    __correlation_id = None
    __health = None

    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__response = Response()
        self.__health = Health()

        status = Health.OK
        errors = []
        errors.extend(self.__health.check_db())
        errors.extend(self.__health.check_io())
        errors.extend(self.__health.check_workers())
        errors.extend(self.__health.check_cache())

        if len(errors) > 0:
            status = Health.NOT_OK

        return JsonResponse(self.__response.send({
            "status": status,
            "errors": errors
        }, self.__correlation_id), status=200 if status == Health.OK else 503)
