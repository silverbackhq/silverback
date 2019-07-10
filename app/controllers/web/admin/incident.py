"""
Incident Web Controller
"""

# Standard Library
import os

# Third Party Library
from django.views import View
from django.http import Http404
from django.shortcuts import render
from django.utils.translation import gettext as _

# Local Library
from app.modules.core.context import Context
from app.modules.core.incident import Incident as IncidentModule
from app.modules.core.decorators import login_if_not_authenticated
from app.modules.core.component import Component as ComponentModule
from app.modules.core.component_group import ComponentGroup as ComponentGroupModule
from app.modules.core.incident_update import IncidentUpdate as IncidentUpdateModule


class IncidentList(View):

    template_name = 'templates/admin/incident/list.html'
    __context = Context()
    __incident = IncidentModule()
    __incident_update = IncidentUpdateModule()
    __component = ComponentModule()
    __component_group = ComponentGroupModule()
    __correlation_id = None

    @login_if_not_authenticated
    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Incidents · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        return render(request, self.template_name, self.__context.get())


class IncidentAdd(View):

    template_name = 'templates/admin/incident/add.html'
    __context = Context()
    __incident = IncidentModule()
    __incident_update = IncidentUpdateModule()
    __component = ComponentModule()
    __component_group = ComponentGroupModule()
    __correlation_id = None

    @login_if_not_authenticated
    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Add an Incident · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        return render(request, self.template_name, self.__context.get())


class IncidentEdit(View):

    template_name = 'templates/admin/incident/edit.html'
    __context = Context()
    __incident = IncidentModule()
    __incident_update = IncidentUpdateModule()
    __component = ComponentModule()
    __component_group = ComponentGroupModule()
    __correlation_id = None

    @login_if_not_authenticated
    def get(self, request, incident_id):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        incident = self.__incident.get_one_by_id(incident_id)

        if not incident:
            raise Http404("Incident not found.")

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Edit Incident · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "incident": incident
        })

        return render(request, self.template_name, self.__context.get())


class IncidentView(View):

    template_name = 'templates/admin/incident/view.html'
    __context = Context()
    __incident = IncidentModule()
    __incident_update = IncidentUpdateModule()
    __component = ComponentModule()
    __component_group = ComponentGroupModule()
    __correlation_id = None

    @login_if_not_authenticated
    def get(self, request, incident_id):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        incident = self.__incident.get_one_by_id(incident_id)

        if not incident:
            raise Http404("Incident not found.")

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("View Incident · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "incident": incident
        })

        return render(request, self.template_name, self.__context.get())
