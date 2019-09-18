"""
    Activity Web Controller
    ~~~~~~~~~~~~~~

    :copyright: silverbackhq
    :license: BSD-3-Clause
"""

# Standard Library
import os

# Third Party Library
from django.views import View
from django.shortcuts import render
from django.utils.translation import gettext as _

# Local Library
from app.modules.core.acl import ACL
from app.modules.core.upgrade import Upgrade
from app.modules.core.context import Context
from app.modules.core.decorators import login_if_not_authenticated


class Activity(View):

    template_name = 'templates/admin/activity.html'
    __context = Context()
    __upgrade = Upgrade()
    __acl = ACL()
    __correlation_id = None

    @login_if_not_authenticated
    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)

        self.__context.push({
            "page_title": _("Activity · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        return render(request, self.template_name, self.__context.get())
