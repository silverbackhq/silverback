"""
User Web Controller
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
from app.modules.core.user import User as User_Module
from app.modules.core.decorators import login_if_not_authenticated


class User_List(View):

    template_name = 'templates/admin/user/list.html'
    __context = Context()
    __user = User_Module()
    __correlation_id = None

    @login_if_not_authenticated
    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"]
        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Users · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        return render(request, self.template_name, self.__context.get())


class User_Add(View):

    template_name = 'templates/admin/user/add.html'
    __context = Context()
    __user = User_Module()
    __correlation_id = None

    @login_if_not_authenticated
    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"]
        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Add a User · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        return render(request, self.template_name, self.__context.get())


class User_Edit(View):

    template_name = 'templates/admin/user/edit.html'
    __context = Context()
    __user = User_Module()
    __correlation_id = None

    @login_if_not_authenticated
    def get(self, request, user_id):

        self.__correlation_id = request.META["X-Correlation-ID"]
        user = self.__user.get_one_by_id(user_id)

        if not user:
            raise Http404("User not found.")

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Edit User · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "user": user
        })

        return render(request, self.template_name, self.__context.get())
