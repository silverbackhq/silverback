"""
Install Web Controller
"""

# standard library
import os

# Django
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.translation import gettext as _

# local Django
from app.modules.core.context import Context
from app.modules.entity.option_entity import Option_Entity
from app.modules.core.install import Install as Install_Module


class Install(View):

    template_name = 'templates/install.html'
    __context = None
    __install = None
    __option_entity = None
    __correlation_id = None

    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"]
        self.__context = Context()
        self.__install = Install_Module()
        self.__option_entity = Option_Entity()

        if self.__install.is_installed():
            return redirect("app.web.login")

        self.__context.push({
            "page_title": _("Installation · %s") % self.__option_entity.get_value_by_key("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        return render(request, self.template_name, self.__context.get())
