"""
Logout Web Controller
"""

# Django
from django.views import View
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.utils.translation import gettext as _

# local Django
from app.modules.core.decorators import login_if_not_authenticated


class Logout(View):

    @login_if_not_authenticated
    def get(self, request):
        logout(request)
        messages.success(request, _("You've been logged out successfully"))
        return redirect("app.web.login")
