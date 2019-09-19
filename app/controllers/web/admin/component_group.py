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
from app.modules.core.component_group import ComponentGroup as ComponentGroupModule


class ComponentGroupList(View):

    template_name = 'templates/admin/component_group/list.html'
    __context = Context()
    __component_group = ComponentGroupModule()
    __correlation_id = None

    @login_if_not_authenticated
    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Component Groups · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        return render(request, self.template_name, self.__context.get())


class ComponentGroupAdd(View):

    template_name = 'templates/admin/component_group/add.html'
    __context = Context()
    __component_group = ComponentGroupModule()
    __correlation_id = None

    @login_if_not_authenticated
    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Add a Component Group · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        return render(request, self.template_name, self.__context.get())


class ComponentGroupEdit(View):

    template_name = 'templates/admin/component_group/edit.html'
    __context = Context()
    __component_group = ComponentGroupModule()
    __correlation_id = None

    @login_if_not_authenticated
    def get(self, request, group_id):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        group = self.__component_group.get_one_by_id(group_id)

        if not group:
            raise Http404("Component group not found.")

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Edit Component Group · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "group": group
        })

        return render(request, self.template_name, self.__context.get())
