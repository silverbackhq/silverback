"""
Register Web Controller
"""

# standard library
import os

# Django
from django.views import View
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.translation import gettext as _

# local Django
from app.modules.core.context import Context
from app.modules.entity.option_entity import Option_Entity
from app.modules.core.decorators import redirect_if_authenticated
from app.modules.core.decorators import redirect_if_not_installed
from app.modules.core.user import User as User_Module


class Register(View):

    template_name = 'templates/register.html'
    __user = None
    __context = None
    __option_entity = None

    @redirect_if_not_installed
    @redirect_if_authenticated
    def get(self, request, token):

        self.__user = User_Module()
        self.__context = Context()
        self.__option_entity = Option_Entity()

        if not self.__user.check_register_request(token):
            messages.error(request, _("Register token is expired or invalid, Please contact system administrator!"))
            return redirect("app.web.login")

        self.__context.autoload_options()
        self.__context.push({
            "page_title": _("Register · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Badger")),
            "register_request": self.__user.get_register_request(token)
        })

        return render(request, self.template_name, self.__context.get())
