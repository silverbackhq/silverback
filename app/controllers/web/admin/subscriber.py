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
from app.modules.core.context import Context
from app.modules.core.subscriber import Subscriber as SubscriberModule
from app.modules.core.decorators import login_if_not_authenticated


class SubscriberList(View):

    template_name = 'templates/admin/subscriber/list.html'
    __context = Context()
    __subscriber = SubscriberModule()
    __correlation_id = None

    @login_if_not_authenticated
    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Subscribers · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        return render(request, self.template_name, self.__context.get())


class SubscriberAdd(View):

    template_name = 'templates/admin/subscriber/add.html'
    __context = Context()
    __subscriber = SubscriberModule()
    __correlation_id = None

    @login_if_not_authenticated
    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Add an Subscriber · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback"))
        })

        return render(request, self.template_name, self.__context.get())


class SubscriberEdit(View):

    template_name = 'templates/admin/subscriber/edit.html'
    __context = Context()
    __subscriber = SubscriberModule()
    __correlation_id = None

    @login_if_not_authenticated
    def get(self, request, subscriber_id):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        subscriber = self.__subscriber.get_one_by_id(subscriber_id)

        if not subscriber:
            raise Http404("Subscriber not found.")

        self.__context.autoload_options()
        self.__context.autoload_user(request.user.id if request.user.is_authenticated else None)
        self.__context.push({
            "page_title": _("Edit Subscriber · %s") % self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "subscriber": subscriber
        })

        return render(request, self.template_name, self.__context.get())
