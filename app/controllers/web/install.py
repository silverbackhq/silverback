"""
Install Web Controller
"""

# Standard Library
import os

# Third Party Library
from django.views import View
from django.shortcuts import render
from django.shortcuts import redirect
from django.utils.translation import gettext as _

# Local Library
from app.modules.core.context import Context
from app.modules.entity.option_entity import OptionEntity
from app.modules.core.install import Install as InstallModule


class Install(View):

    template_name = 'templates/install.html'
    __context = None
    __install = None
    __option_entity = None
    __correlation_id = None

    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__context = Context()
        self.__install = InstallModule()
        self.__option_entity = OptionEntity()

        if self.__install.is_installed():
            return redirect("app.web.login")

        self.__context.push({
            "page_title": _("Installation · %s") % self.__option_entity.get_value_by_key("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        return render(request, self.template_name, self.__context.get())
