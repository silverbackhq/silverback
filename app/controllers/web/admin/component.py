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
from app.modules.core.context import Context
from app.modules.core.decorators import login_if_not_authenticated
from app.modules.core.component import Component as ComponentModule


class ComponentList(View):
    """Component List Page Controller"""

    template_name = 'templates/admin/component/list.html'

    @login_if_not_authenticated
    def get(self, request):

        self.__context = Context()
        self.__component = ComponentModule()
        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Components · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        return render(request, self.template_name, self.__context.get())


class ComponentAdd(View):
    """Component Add Page Controller"""

    template_name = 'templates/admin/component/add.html'

    @login_if_not_authenticated
    def get(self, request):

        self.__context = Context()
        self.__component = ComponentModule()
        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Add a Component · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "groups": self.__component.get_all_groups()
        })

        return render(request, self.template_name, self.__context.get())


class ComponentEdit(View):
    """Component Edit Page Controller"""

    template_name = 'templates/admin/component/edit.html'

    @login_if_not_authenticated
    def get(self, request, component_id):

        self.__context = Context()
        self.__component = ComponentModule()
        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        component = self.__component.get_one_by_id(component_id)

        if not component:
            raise Http404("Component not found.")

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Edit Component · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "component": component,
            "groups": self.__component.get_all_groups()
        })

        return render(request, self.template_name, self.__context.get())
