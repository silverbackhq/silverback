"""
Login Web Controller
"""

from django.views import View
from django.http import JsonResponse
from app.modules.core.response import Response
from app.modules.core.health import Health
from app.modules.util.helpers import Helpers
from django.utils.translation import gettext as _


class HealthCheck(View):

    __response = None
    __correlation_id = None
    __health = None
    __helpers = None
    __logger = None

    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__response = Response()
        self.__health = Health()
        self.__helpers = Helpers()
        self.__logger = self.__helpers.get_logger(__name__)

        status = Health.OK
        errors = []
        errors.extend(self.__health.check_db())
        errors.extend(self.__health.check_io())
        errors.extend(self.__health.check_workers())

        if len(errors) > 0:
            status = Health.NOT_OK
            self.__logger.error(_("Health Check Result: %(status)s %(errors)s {'correlationId':'%(correlationId)s'}") % {
                "status": status,
                "errors": self.__helpers.json_dumps(errors),
                "correlationId": self.__correlation_id
            })
        else:
            self.__logger.debug(_("Health Check Result: %(status)s %(errors)s {'correlationId':'%(correlationId)s'}") % {
                "status": status,
                "errors": self.__helpers.json_dumps(errors),
                "correlationId": self.__correlation_id
            })

        return JsonResponse(self.__response.send({
            "status": status
        }, self.__correlation_id), status=200 if status == Health.OK else 503)
