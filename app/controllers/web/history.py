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
from django.http import HttpResponse
from feedgen.feed import FeedGenerator

# Local Library
from app.modules.core.context import Context
from app.modules.entity.option_entity import OptionEntity
from app.modules.core.decorators import redirect_if_not_installed


class AtomHistory(View):

    __context = None
    __option_entity = None
    __fg = None
    __correlation_id = None

    @redirect_if_not_installed
    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__fg = FeedGenerator()
        self.__context = Context()
        self.__option_entity = OptionEntity()

        self.__context.autoload_options()
        self.__context.push({
            "page_title": self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "is_authenticated": request.user and request.user.is_authenticated
        })

        self.__fg.id('http://silverbackhq.org')
        self.__fg.title('Some Testfeed')
        self.__fg.author({'name': 'John Doe', 'email': 'john@silverbackhq.org'})
        self.__fg.link(href='http://example.com', rel='alternate')
        self.__fg.logo('http://ex.com/logo.jpg')
        self.__fg.subtitle('This is a cool feed!')
        self.__fg.link(href='http://silverbackhq.org/test.atom', rel='self')
        self.__fg.language('en')

        return HttpResponse(self.__fg.atom_str(), content_type='text/xml')


class RssHistory(View):

    __context = None
    __option_entity = None
    __fg = None
    __correlation_id = None

    @redirect_if_not_installed
    def get(self, request):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__fg = FeedGenerator()
        self.__context = Context()
        self.__option_entity = OptionEntity()

        self.__context.autoload_options()
        self.__context.push({
            "page_title": self.__context.get("app_name", os.getenv("APP_NAME", "Silverback")),
            "is_authenticated": request.user and request.user.is_authenticated
        })

        self.__fg.id('http://silverbackhq.org')
        self.__fg.title('Some Testfeed')
        self.__fg.author({'name': 'John Doe', 'email': 'john@silverbackhq.org'})
        self.__fg.link(href='http://example.com', rel='alternate')
        self.__fg.logo('http://ex.com/logo.jpg')
        self.__fg.subtitle('This is a cool feed!')
        self.__fg.link(href='http://silverbackhq.org/test.atom', rel='self')
        self.__fg.language('en')

        return HttpResponse(self.__fg.atom_str(), content_type='text/xml')
