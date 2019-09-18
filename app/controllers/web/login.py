"""
    Login Web Controller
    ~~~~~~~~~~~~~~

    :copyright: silverbackhq
    :license: BSD-3-Clause
"""

# Standard Library
import os

# Third Party Library
from django.shortcuts import reverse
from django.views import View
from django.shortcuts import render
from django.utils.translation import gettext as _

# Local Library
from app.modules.core.context import Context
from app.modules.entity.option_entity import OptionEntity
from app.modules.core.decorators import redirect_if_authenticated
from app.modules.core.decorators import redirect_if_not_installed


class Login(View):

    template_name = 'templates/login.html'
    __context = None
    __option_entity = None
    __correlation_id = None

    @redirect_if_not_installed
    @redirect_if_authenticated
    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__context = Context()
        self.__option_entity = OptionEntity()

        self.__context.autoload_options()
        self.__context.push({
            "page_title": _("Login · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        if "redirect" in request.GET:
            self.__context.push({
                "redirect_url": request.GET["redirect"]
            })
        else:
            self.__context.push({
                "redirect_url": reverse("app.web.admin.dashboard")
            })

        return render(request, self.template_name, self.__context.get())
