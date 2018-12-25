"""
Forbidden Access Views
"""

# Django
from django.http import JsonResponse
from django.utils.translation import gettext as _

# local Django
from app.modules.core.response import Response


def csrf_failure(request, reason=""):
    response = Response()
    return JsonResponse(response.send_private_failure([{
        "type": "error",
        "message": _("Error! Access forbidden due to invalid CSRF token.")
    }]))
