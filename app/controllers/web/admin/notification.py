"""
Notification Web Controller
"""

# standard library
import os

# Django
from django.views import View
from django.shortcuts import render
from django.utils.translation import gettext as _

# local Django
from app.modules.core.context import Context
from app.modules.core.acl import ACL
from app.modules.core.decorators import login_if_not_authenticated


class Notification(View):

    template_name = 'templates/admin/notification.html'
    __context = Context()
    __acl = ACL()

    @login_if_not_authenticated
    def get(self, request):

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)

        self.__context.push({
            "page_title": _("Notification · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Badger"))
        })

        return render(request, self.template_name, self.__context.get())
