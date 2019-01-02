"""
Component Groups Web Controller
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
from app.modules.core.component_group import Component_Group as Component_Group_Module
from app.modules.core.decorators import login_if_not_authenticated


class Component_Group_List(View):

    template_name = 'templates/admin/component_group/list.html'
    __context = Context()
    __component_group = Component_Group_Module()

    @login_if_not_authenticated
    def get(self, request):

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Component Groups · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Badger"))
        })

        return render(request, self.template_name, self.__context.get())


class Component_Group_Add(View):

    template_name = 'templates/admin/component_group/add.html'
    __context = Context()
    __component_group = Component_Group_Module()

    @login_if_not_authenticated
    def get(self, request):

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Add a Component Group · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Badger"))
        })

        return render(request, self.template_name, self.__context.get())


class Component_Group_Edit(View):

    template_name = 'templates/admin/component_group/edit.html'
    __context = Context()
    __component_group = Component_Group_Module()

    @login_if_not_authenticated
    def get(self, request, group_id):

        group = True

        if not group:
            raise Http404("Component group not found.")

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Edit Component Group · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Badger")),
            "group": {
                "id": group_id
            }
        })

        return render(request, self.template_name, self.__context.get())
