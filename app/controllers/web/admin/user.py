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
from django.http import Http404
from django.shortcuts import render
from django.utils.translation import gettext as _

# Local Library
from app.controllers.controller import Controller
from app.modules.core.user import User as UserModule
from app.modules.core.decorators import login_if_not_authenticated_or_no_permission


class UserList(View, Controller):
    """User List Page Controller"""

    template_name = 'templates/admin/user/list.html'

    @login_if_not_authenticated_or_no_permission("manage_settings")
    def get(self, request):

        self.__user = UserModule()
        self.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.context_push({
            "page_title": _("Users · %s") % self.context_get("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        return render(request, self.template_name, self.context_get())


class UserAdd(View, Controller):
    """User Add Page Controller"""

    template_name = 'templates/admin/user/add.html'

    @login_if_not_authenticated_or_no_permission("manage_settings")
    def get(self, request):

        self.__user = UserModule()
        self.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.context_push({
            "page_title": _("Add a User · %s") % self.context_get("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        return render(request, self.template_name, self.context_get())


class UserEdit(View, Controller):
    """User Edit Page Controller"""

    template_name = 'templates/admin/user/edit.html'

    @login_if_not_authenticated_or_no_permission("manage_settings")
    def get(self, request, user_id):

        self.__user = UserModule()
        user = self.__user.get_one_by_id(user_id)

        if not user:
            raise Http404("User not found.")

        self.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.context_push({
            "page_title": _("Edit User · %s") % self.context_get("app_name", os.getenv("APP_NAME", "Silverback")),
            "user": user
        })

        return render(request, self.template_name, self.context_get())
