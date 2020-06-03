# Copyright 2019 Silverbackhq
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Standard Library
import os

# Third Party Library
from django.views import View
from django.http import Http404
from django.shortcuts import render
from django.utils.translation import gettext as _

# Local Library
from app.controllers.controller import Controller
from app.modules.core.incident import Incident as IncidentModule
from app.modules.core.decorators import login_if_not_authenticated
from app.modules.core.component import Component as ComponentModule
from app.modules.core.component_group import ComponentGroup as ComponentGroupModule
from app.modules.core.incident_update import IncidentUpdate as IncidentUpdateModule


class IncidentList(View, Controller):
    """Incident List Page Controller"""

    template_name = 'templates/admin/incident/list.html'

    @login_if_not_authenticated
    def get(self, request):

        self.__incident = IncidentModule()
        self.__incident_update = IncidentUpdateModule()
        self.__component = ComponentModule()
        self.__component_group = ComponentGroupModule()
        self.autoload_options()
        self.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.context_push({
            "page_title": _("Incidents · %s") % self.context_get("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        return render(request, self.template_name, self.context_get())


class IncidentAdd(View, Controller):
    """Incident Add Page Controller"""

    template_name = 'templates/admin/incident/add.html'

    @login_if_not_authenticated
    def get(self, request):

        self.__incident = IncidentModule()
        self.__incident_update = IncidentUpdateModule()
        self.__component = ComponentModule()
        self.__component_group = ComponentGroupModule()
        self.autoload_options()
        self.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.context_push({
            "page_title": _("Add an Incident · %s") % self.context_get("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        return render(request, self.template_name, self.context_get())


class IncidentEdit(View, Controller):
    """Incident Edit Page Controller"""

    template_name = 'templates/admin/incident/edit.html'

    @login_if_not_authenticated
    def get(self, request, incident_id):

        self.__incident = IncidentModule()
        self.__incident_update = IncidentUpdateModule()
        self.__component = ComponentModule()
        self.__component_group = ComponentGroupModule()
        incident = self.__incident.get_one_by_id(incident_id)

        if not incident:
            raise Http404("Incident not found.")

        self.autoload_options()
        self.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.context_push({
            "page_title": _("Edit Incident · %s") % self.context_get("app_name", os.getenv("APP_NAME", "Silverback")),
            "incident": incident
        })

        return render(request, self.template_name, self.context_get())


class IncidentView(View, Controller):
    """Incident View Page Controller"""

    template_name = 'templates/admin/incident/view.html'

    @login_if_not_authenticated
    def get(self, request, incident_id):

        self.__incident = IncidentModule()
        self.__incident_update = IncidentUpdateModule()
        self.__component = ComponentModule()
        self.__component_group = ComponentGroupModule()
        incident = self.__incident.get_one_by_id(incident_id)

        if not incident:
            raise Http404("Incident not found.")

        self.autoload_options()
        self.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.context_push({
            "page_title": _("View Incident · %s") % self.context_get("app_name", os.getenv("APP_NAME", "Silverback")),
            "incident": incident
        })

        return render(request, self.template_name, self.context_get())
