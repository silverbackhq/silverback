"""
Profile Web Controller
"""

# standard library
import os

# Django
from django.views import View
from django.shortcuts import render
from django.utils.translation import gettext as _

# local Django
from app.modules.core.context import Context
from app.modules.core.profile import Profile
from app.modules.core.decorators import login_if_not_authenticated


class Profile(View):

    template_name = 'templates/admin/profile.html'
    __context = Context()
    __profile = Profile()
    __user_id = None
    __correlation_id = None

    @login_if_not_authenticated
    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"]
        self.__user_id = request.user.id
        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Profile · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        self.__context.push(self.__profile.get_profile(self.__user_id))

        return render(request, self.template_name, self.__context.get())
