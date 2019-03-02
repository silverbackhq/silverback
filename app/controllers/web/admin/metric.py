"""
Metrics Web Controller
"""

# standard library
import os
import json

# Django
from django.views import View
from django.http import Http404
from django.shortcuts import render
from django.utils.translation import gettext as _

# local Django
from app.modules.core.context import Context
from app.modules.core.metric import Metric as Metric_Module
from app.modules.core.decorators import login_if_not_authenticated


class Metric_List(View):

    template_name = 'templates/admin/metric/list.html'
    __context = Context()
    __metric = Metric_Module()

    @login_if_not_authenticated
    def get(self, request):

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Metrics · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        return render(request, self.template_name, self.__context.get())


class Metric_Add(View):

    template_name = 'templates/admin/metric/add.html'
    __context = Context()
    __metric = Metric_Module()

    @login_if_not_authenticated
    def get(self, request):

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Add a Metric · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        return render(request, self.template_name, self.__context.get())


class Metric_Edit(View):

    template_name = 'templates/admin/metric/edit.html'
    __context = Context()
    __metric = Metric_Module()

    @login_if_not_authenticated
    def get(self, request, metric_id):

        metric = self.__metric.get_one_by_id(metric_id)

        if not metric:
            raise Http404("Metric not found.")

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Edit Metric · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "metric": metric
        })

        metric["data"] = json.loads(metric["data"])

        return render(request, self.template_name, self.__context.get())
