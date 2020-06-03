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
from django.shortcuts import render
from django.utils.translation import gettext as _

# Local Library
from app.controllers.controller import Controller
from app.modules.core.decorators import login_if_not_authenticated
from app.modules.core.dashboard import Dashboard as DashboardModule


class Dashboard(View, Controller):
    """Dashboard Page Controller"""

    template_name = 'templates/admin/dashboard.html'

    @login_if_not_authenticated
    def get(self, request):

        self.__dashboard = DashboardModule()
        self.autoload_options()
        self.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.context_push({
            "page_title": _("Dashboard · %s") % self.context_get("app_name", os.getenv("APP_NAME", "Silverback")),
            "count": {
                "incidents": self.__dashboard.incidents_count(),
                "subscribers": self.__dashboard.subscribers_count(),
                "components": self.__dashboard.components_count(),
                "component_groups": self.__dashboard.component_groups_count(),
                "metrics": self.__dashboard.metrics_count(),
                "users": self.__dashboard.users_count(),
                "delivered_notifications": self.__dashboard.notifications_count("success"),
                "failed_notifications": self.__dashboard.notifications_count("failed")
            },
            "chart": {
                "subscribers": self.__dashboard.subscribers_chart(),
                "components": self.__dashboard.components_chart(),
                "delivered_notifications": self.__dashboard.notifications_chart("success", 14),
                "failed_notifications": self.__dashboard.notifications_chart("failed", 14),
                "incidents": self.__dashboard.incidents_chart()
            },
            "open_incidents": self.__dashboard.get_open_incidents(),
            "affected_components": self.__dashboard.get_affected_components()
        })

        return render(request, self.template_name, self.context_get())
