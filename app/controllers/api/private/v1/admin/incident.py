"""
User API Endpoint
"""

# Django
from django.views import View
from django.http import JsonResponse
from django.utils.translation import gettext as _
from django.urls import reverse

# local Django
from app.modules.validation.form import Form
from app.modules.util.helpers import Helpers
from app.modules.core.request import Request
from app.modules.core.response import Response
from app.modules.core.incident import Incident as Incident_Module


class Incidents(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __incident = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__incident = Incident_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def post(self, request):
        pass

    def get(self, request):

        self.__request.set_request(request)

        request_data = self.__request.get_request_data("get", {
            "offset": "",
            "limit": ""
        })

        try:
            offset = int(request_data["offset"])
            limit = int(request_data["limit"])
        except Exception:
            offset = 0
            limit = 0

        return JsonResponse(self.__response.send_private_success([], {
            'incidents': self.__format_incidents(self.__incident.get_all(offset, limit)),
            'metadata': {
                'offset': offset,
                'limit': limit,
                'count': self.__incident.count_all()
            }
        }))

    def __format_incidents(self, incidents):
        incidents_list = []

        for incident in incidents:
            incidents_list.append({
                "id": incident.id,
                "name": incident.name,
                "uri": incident.uri,
                "status": incident.status,
                "created_at": incident.created_at.strftime("%b %d %Y %H:%M:%S"),
                "view_url": reverse("app.web.admin.incident.view", kwargs={'incident_id': incident.id}),
                "edit_url": reverse("app.web.admin.incident.edit", kwargs={'incident_id': incident.id}),
                "delete_url": reverse("app.api.private.v1.admin.incident.endpoint", kwargs={'incident_id': incident.id})
            })

        return incidents_list


class Incident(View):

    __request = None
    __response = None
    __helpers = None
    __form = None
    __logger = None
    __user_id = None
    __incident = None

    def __init__(self):
        self.__request = Request()
        self.__response = Response()
        self.__helpers = Helpers()
        self.__form = Form()
        self.__incident = Incident_Module()
        self.__logger = self.__helpers.get_logger(__name__)

    def get(self, request, incident_id):
        pass

    def post(self, request, incident_id):
        pass

    def delete(self, request, incident_id):

        self.__user_id = request.user.id

        if self.__incident.delete_one_by_id(incident_id):
            return JsonResponse(self.__response.send_private_success([{
                "type": "success",
                "message": _("Incident deleted successfully.")
            }]))

        else:
            return JsonResponse(self.__response.send_private_failure([{
                "type": "error",
                "message": _("Error! Something goes wrong while deleting incident.")
            }]))
