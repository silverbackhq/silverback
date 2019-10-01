# Copyright 2019 Silverbackhq
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
    """Login Page Controller"""

    template_name = 'templates/login.html'

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
