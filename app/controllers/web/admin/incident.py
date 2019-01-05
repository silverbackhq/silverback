"""
Components Web Controller
"""

# standard library
import os

# Django
from django.views import View
from django.http import Http404
from django.shortcuts import render
from django.utils.translation import gettext as _

# local Django
from app.modules.core.context import Context
from app.modules.core.component import Component as Component_Module
from app.modules.core.component_group import Component_Group as Component_Group_Module
from app.modules.core.incident import Incident as Incident_Module
from app.modules.core.incident_update import Incident_Update as Incident_Update_Module
from app.modules.core.decorators import login_if_not_authenticated


class Incident_List(View):

    template_name = 'templates/admin/incident/list.html'
    __context = Context()
    __incident = Incident_Module()
    __incident_update = Incident_Update_Module()
    __component = Component_Module()
    __component_group = Component_Group_Module()

    @login_if_not_authenticated
    def get(self, request):

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Incidents · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Badger"))
        })

        return render(request, self.template_name, self.__context.get())


class Incident_Add(View):

    template_name = 'templates/admin/incident/add.html'
    __context = Context()
    __incident = Incident_Module()
    __incident_update = Incident_Update_Module()
    __component = Component_Module()
    __component_group = Component_Group_Module()

    @login_if_not_authenticated
    def get(self, request):

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Add an Incident · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Badger"))
        })

        return render(request, self.template_name, self.__context.get())


class Incident_Edit(View):

    template_name = 'templates/admin/incident/edit.html'
    __context = Context()
    __incident = Incident_Module()
    __incident_update = Incident_Update_Module()
    __component = Component_Module()
    __component_group = Component_Group_Module()

    @login_if_not_authenticated
    def get(self, request, incident_id):

        incident = self.__incident.get_one_by_id(incident_id)

        if not incident:
            raise Http404("Incident not found.")

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Edit Incident · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Badger")),
            "incident": incident
        })

        return render(request, self.template_name, self.__context.get())


class Incident_View(View):

    template_name = 'templates/admin/incident/view.html'
    __context = Context()
    __incident = Incident_Module()
    __incident_update = Incident_Update_Module()
    __component = Component_Module()
    __component_group = Component_Group_Module()

    @login_if_not_authenticated
    def get(self, request, incident_id):

        incident = incident_id

        if not incident:
            raise Http404("Incident not found.")

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("View Incident · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Badger")),
            "incident": incident
        })

        return render(request, self.template_name, self.__context.get())
