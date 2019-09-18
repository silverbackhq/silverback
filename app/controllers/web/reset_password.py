"""
    Reset Password Web Controller
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
from app.modules.entity.option_entity import OptionEntity
from app.modules.core.decorators import redirect_if_authenticated
from app.modules.core.decorators import redirect_if_not_installed
from app.modules.core.reset_password import ResetPassword as ResetPasswordModule


class ResetPassword(View):

    template_name = 'templates/reset_password.html'
    __reset_password_core = None
    __context = None
    __option_entity = None
    __correlation_id = None

    @redirect_if_not_installed
    @redirect_if_authenticated
    def get(self, request, token):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__reset_password_core = ResetPasswordModule()
        self.__context = Context()
        self.__option_entity = OptionEntity()

        self.__context.autoload_options()
        self.__context.push({
            "page_title": _("Reset Password · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "reset_token": token
        })

        if not self.__reset_password_core.check_token(token):
            messages.error(request, _("Reset token is expired or invalid, Please request another token!"))
            return redirect("app.web.forgot_password")

        return render(request, self.template_name, self.__context.get())
