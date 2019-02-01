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
from app.modules.core.decorators import login_if_not_authenticated


class Component_List(View):

    template_name = 'templates/admin/component/list.html'
    __context = Context()
    __component = Component_Module()

    @login_if_not_authenticated
    def get(self, request):

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Components · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        return render(request, self.template_name, self.__context.get())


class Component_Add(View):

    template_name = 'templates/admin/component/add.html'
    __context = Context()
    __component = Component_Module()

    @login_if_not_authenticated
    def get(self, request):

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Add a Component · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "groups": self.__component.get_all_groups()
        })

        return render(request, self.template_name, self.__context.get())


class Component_Edit(View):

    template_name = 'templates/admin/component/edit.html'
    __context = Context()
    __component = Component_Module()

    @login_if_not_authenticated
    def get(self, request, component_id):

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
