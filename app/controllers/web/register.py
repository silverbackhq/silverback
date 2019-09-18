"""
    Register Web Controller
    ~~~~~~~~~~~~~~

    :copyright: silverbackhq
    :license: BSD-3-Clause
"""

# Standard Library
import os

# Third Party Library
from django.views import View
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _

# Local Library
from app.modules.core.context import Context
from app.modules.core.user import User as UserModule
from app.modules.entity.option_entity import OptionEntity
from app.modules.core.decorators import redirect_if_authenticated
from app.modules.core.decorators import redirect_if_not_installed


class Register(View):

    template_name = 'templates/register.html'
    __user = None
    __context = None
    __option_entity = None
    __correlation_id = None

    @redirect_if_not_installed
    @redirect_if_authenticated
    def get(self, request, token):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__user = UserModule()
        self.__context = Context()
        self.__option_entity = OptionEntity()

        if not self.__user.check_register_request(token):
            messages.error(request, _("Register token is expired or invalid, Please contact system administrator!"))
            return redirect("app.web.login")

        self.__context.autoload_options()
        self.__context.push({
            "page_title": _("Register · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "register_request": self.__user.get_register_request_by_token(token)
        })

        return render(request, self.template_name, self.__context.get())
