"""
Forgot Password Web Controller
"""

# standard library
import os

# Django
from django.views import View
from django.shortcuts import render
from django.utils.translation import gettext as _

# local Django
from app.modules.core.context import Context
from app.modules.entity.option_entity import Option_Entity
from app.modules.core.decorators import redirect_if_authenticated
from app.modules.core.decorators import redirect_if_not_installed


class Forgot_Password(View):

    template_name = 'templates/forgot_password.html'
    __context = None
    __option_entity = None
    __correlation_id = None

    @redirect_if_not_installed
    @redirect_if_authenticated
    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"]
        self.__context = Context()
        self.__option_entity = Option_Entity()

        self.__context.autoload_options()
        self.__context.push({
            "page_title": _("Forgot Password · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        return render(request, self.template_name, self.__context.get())
