"""
Status Page Index Web Controller
"""

# standard library
import os

# Django
from django.views import View
from django.shortcuts import render

# local Django
from app.modules.core.context import Context
from app.modules.entity.option_entity import Option_Entity
from app.modules.core.decorators import redirect_if_not_installed


class Status_Page_Index(View):

    template_name = 'templates/status_page_index.html'
    __context = None
    __option_entity = None

    @redirect_if_not_installed
    def get(self, request):

        self.__context = Context()
        self.__option_entity = Option_Entity()

        self.__context.autoload_options()
        self.__context.push({
            "page_title": self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "is_authenticated": request.user and request.user.is_authenticated
        })

        return render(request, self.template_name, self.__context.get())


class Status_Page_History(View):

    template_name = 'templates/status_page_history.html'
    __context = None
    __option_entity = None

    @redirect_if_not_installed
    def get(self, request):

        self.__context = Context()
        self.__option_entity = Option_Entity()

        self.__context.autoload_options()
        self.__context.push({
            "page_title": self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "is_authenticated": request.user and request.user.is_authenticated
        })

        return render(request, self.template_name, self.__context.get())


class Status_Page_Single(View):

    template_name = 'templates/status_page_single.html'
    __context = None
    __option_entity = None

    @redirect_if_not_installed
    def get(self, request, uri):

        self.__context = Context()
        self.__option_entity = Option_Entity()

        self.__context.autoload_options()
        self.__context.push({
            "page_title": self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "is_authenticated": request.user and request.user.is_authenticated,
            "uri": uri
        })

        return render(request, self.template_name, self.__context.get())
