"""
Dashboard Web Controller
"""

# standard library
import os

# Django
from django.views import View
from django.shortcuts import render
from django.utils.translation import gettext as _

# local Django
from app.modules.core.context import Context
from app.modules.core.dashboard import Dashboard as Dashboard_Module
from app.modules.core.decorators import login_if_not_authenticated


class Dashboard(View):

    template_name = 'templates/admin/dashboard.html'
    __context = Context()
    __dashboard = Dashboard_Module()

    @login_if_not_authenticated
    def get(self, request):

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Dashboard · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "count": {
                "incidents": self.__dashboard.incidents_count(),
                "subscribers": self.__dashboard.subscribers_count(),
                "components": self.__dashboard.components_count(),
                "component_groups": self.__dashboard.component_groups_count(),
                "metrics": self.__dashboard.metrics_count(),
                "users": self.__dashboard.users_count(),
                "delivered_notifications": self.__dashboard.delivered_notifications_count(),
                "failed_notifications": self.__dashboard.failed_notifications_count()
            },
            "chart": {
                "subscribers": self.__dashboard.subscribers_chart(),
                "components": self.__dashboard.components_chart(),
                "delivered_notifications": self.__dashboard.delivered_notifications_chart(),
                "failed_notifications": self.__dashboard.failed_notifications_chart(),
                "incidents": self.__dashboard.incidents_chart()
            }
        })

        return render(request, self.template_name, self.__context.get())
