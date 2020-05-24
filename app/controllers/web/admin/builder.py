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
import json

# Third Party Library
from django.views import View
from django.shortcuts import render
from django.utils.translation import gettext as _

# Local Library
from app.modules.core.context import Context
from app.controllers.controller import Controller
from app.modules.core.metric import Metric as MetricModule
from app.modules.core.component import Component as ComponentModule
from app.modules.core.component_group import ComponentGroup as ComponentGroupModule
from app.modules.core.decorators import login_if_not_authenticated_or_no_permission


class Builder(View, Controller):
    """Builder Page Controller"""

    template_name = 'templates/admin/builder.html'

    @login_if_not_authenticated_or_no_permission("manage_settings")
    def get(self, request):

        self.__context = Context()
        self.__metric = MetricModule()
        self.__component = ComponentModule()
        self.__component_group = ComponentGroupModule()
        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.load_options({
            "builder_headline": "",
            "builder_favicon_url": "",
            "builder_logo_url": "",
            "builder_about": "",
            "builder_components": json.dumps([]),
            "builder_metrics": json.dumps([])
        })
        self.__context.push({
            "page_title": _("Status Page Builder · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "groups": self.__format_groups(self.__component.get_all_groups()),
            "components": self.__format_components(self.__component.get_all()),
            "metrics": self.__format_metrics(self.__metric.get_all())
        })

        self.__context.push({
            "builder_components": json.loads(str(self.__context.get("builder_components"))),
            "builder_metrics": json.loads(str(self.__context.get("builder_metrics")))
        })

        return render(request, self.template_name, self.__context.get())

    def __format_components(self, components):
        components_list = []

        for component in components:
            components_list.append({
                "id": "c-%d" % component.id,
                "name": component.name
            })

        return components_list

    def __format_groups(self, groups):
        groups_list = []

        for group in groups:
            groups_list.append({
                "id": "g-%d" % group.id,
                "name": group.name
            })

        return groups_list

    def __format_metrics(self, metrics):
        metrics_list = []

        for metric in metrics:
            metrics_list.append({
                "id": "m-%d" % metric.id,
                "title": metric.title
            })

        return metrics_list
