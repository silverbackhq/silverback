"""
Subscriber Web Controller
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
from app.modules.core.subscriber import Subscriber as Subscriber_Module
from app.modules.core.decorators import login_if_not_authenticated


class Subscriber_List(View):

    template_name = 'templates/admin/subscriber/list.html'
    __context = Context()
    __subscriber = Subscriber_Module()
    __correlation_id = None

    @login_if_not_authenticated
    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"]
        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Subscribers · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        return render(request, self.template_name, self.__context.get())


class Subscriber_Add(View):

    template_name = 'templates/admin/subscriber/add.html'
    __context = Context()
    __subscriber = Subscriber_Module()
    __correlation_id = None

    @login_if_not_authenticated
    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"]
        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Add an Subscriber · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        return render(request, self.template_name, self.__context.get())


class Subscriber_Edit(View):

    template_name = 'templates/admin/subscriber/edit.html'
    __context = Context()
    __subscriber = Subscriber_Module()
    __correlation_id = None

    @login_if_not_authenticated
    def get(self, request, subscriber_id):

        self.__correlation_id = request.META["X-Correlation-ID"]
        subscriber = self.__subscriber.get_one_by_id(subscriber_id)

        if not subscriber:
            raise Http404("Subscriber not found.")

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Edit Subscriber · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "subscriber": subscriber
        })

        return render(request, self.template_name, self.__context.get())
