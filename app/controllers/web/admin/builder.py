"""
Builder Web Controller
"""

# standard library
import os
import json

# Django
from django.views import View
from django.shortcuts import render
from django.utils.translation import gettext as _

# local Django
from app.modules.core.context import Context
from app.modules.core.metric import Metric as Metric_Module
from app.modules.core.decorators import login_if_not_authenticated
from app.modules.core.component import Component as Component_Module
from app.modules.core.component_group import Component_Group as Component_Group_Module


class Builder(View):

    template_name = 'templates/admin/builder.html'
    __context = Context()
    __metric = Metric_Module()
    __component = Component_Module()
    __component_group = Component_Group_Module()
    __correlation_id = None

    @login_if_not_authenticated
    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.load_options({
            "builder_headline": "",
            "builder_fav_icon_url": "",
            "builder_cover_image_url": "",
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
