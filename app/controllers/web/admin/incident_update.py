"""
    Incident Update Web Controller
    ~~~~~~~~~~~~~~

    :copyright: silverbackhq
    :license: BSD-3-Clause
"""

# Standard Library
import os
import markdown2

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
from app.modules.core.incident_update_component import IncidentUpdateComponent as IncidentUpdateComponentModule
from app.modules.core.incident_update_notification import IncidentUpdateNotification as IncidentUpdateNotificationModule


class IncidentUpdateAdd(View):

    template_name = 'templates/admin/incident/update/add.html'
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
            "page_title": _("Add Incident Update  · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "incident": incident
        })

        return render(request, self.template_name, self.__context.get())


class IncidentUpdateView(View):

    template_name = 'templates/admin/incident/update/view.html'
    __context = Context()
    __incident = IncidentModule()
    __incident_update = IncidentUpdateModule()
    __incident_update_component = IncidentUpdateComponentModule()
    __component = ComponentModule()
    __component_group = ComponentGroupModule()
    __incident_update_notification = IncidentUpdateNotificationModule()
    __correlation_id = None

    @login_if_not_authenticated
    def get(self, request, incident_id, update_id):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        incident = self.__incident.get_one_by_id(incident_id)

        if not incident:
            raise Http404("Incident not found.")

        update = self.__incident_update.get_one_by_id(update_id)

        if not update:
            raise Http404("Incident update not found.")

        update["datetime"] = update["datetime"].strftime("%b %d %Y %H:%M:%S")
        update["message"] = markdown2.markdown(update["message"])
        update["notified_subscribers"] = self.__incident_update_notification.count_by_update_status(
            update["id"],
            IncidentUpdateNotificationModule.SUCCESS
        )
        update["failed_subscribers"] = self.__incident_update_notification.count_by_update_status(
            update["id"],
            IncidentUpdateNotificationModule.FAILED
        )

        components = self.__format_components(self.__component.get_all())
        affected_components = self.__format_affected_components(self.__incident_update_component.get_all(update_id))

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("View Incident Update  · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "update": update,
            "incident": incident,
            "components": components,
            "affected_components": affected_components
        })

        return render(request, self.template_name, self.__context.get())

    def __format_components(self, components):
        components_list = []

        for component in components:
            components_list.append({
                "id": component.id,
                "name": component.name
            })

        return components_list

    def __format_affected_components(self, affected_components):
        affected_components_list = []

        for affected_component in affected_components:
            affected_components_list.append({
                "id": affected_component.id,
                "component_id": affected_component.component.id,
                "component_name": affected_component.component.name,
                "type": affected_component.type
            })

        return affected_components_list


class IncidentUpdateEdit(View):

    template_name = 'templates/admin/incident/update/edit.html'
    __context = Context()
    __incident = IncidentModule()
    __incident_update = IncidentUpdateModule()
    __component = ComponentModule()
    __component_group = ComponentGroupModule()
    __correlation_id = None

    @login_if_not_authenticated
    def get(self, request, incident_id, update_id):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        incident = self.__incident.get_one_by_id(incident_id)

        if not incident:
            raise Http404("Incident not found.")

        update = self.__incident_update.get_one_by_id(update_id)

        if not update:
            raise Http404("Incident update not found.")

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Edit Incident Update  · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "update": update,
            "incident": incident
        })

        return render(request, self.template_name, self.__context.get())
