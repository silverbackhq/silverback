"""
    Forbidden Access Views
    ~~~~~~~~~~~~~~

    :copyright: silverbackhq
    :license: BSD-3-Clause
"""

# Third Party Library
from django.http import JsonResponse
from django.utils.translation import gettext as _

# Local Library
from app.modules.core.response import Response


def csrf_failure(request, reason=""):
    correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
    response = Response()
    return JsonResponse(response.send_private_failure([{
        "type": "error",
        "message": _("Error! Access forbidden due to invalid CSRF token.")
    }], {}, correlation_id))
