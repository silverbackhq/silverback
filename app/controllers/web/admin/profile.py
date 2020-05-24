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
from django.views import View
from django.shortcuts import render
from django.utils.translation import gettext as _

# Local Library
from app.controllers.controller import Controller
from app.modules.core.profile import Profile as ProfileModule
from app.modules.core.decorators import login_if_not_authenticated


class Profile(View, Controller):
    """Profile Page Controller"""

    template_name = 'templates/admin/profile.html'

    @login_if_not_authenticated
    def get(self, request):

        self.__profile = ProfileModule()
        self.__user_id = request.user.id
        self.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.context_push({
            "page_title": _("Profile · %s") % self.context_get("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        self.context_push(self.__profile.get_profile(self.__user_id))

        return render(request, self.template_name, self.context_get())
