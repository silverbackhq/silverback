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
from app.controllers.controller import Controller
from app.modules.core.decorators import redirect_if_not_installed


class AtomHistory(View, Controller):
    """Atom History Page Controller"""

    @redirect_if_not_installed
    def get(self, request):

        self.__fg = FeedGenerator()
        self.autoload_options()
        self.context_push({
            "page_title": self.context_get("app_name", os.getenv("APP_NAME", "Silverback")),
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


class RssHistory(View, Controller):
    """RSS History Page Controller"""

    @redirect_if_not_installed
    def get(self, request):

        self.__fg = FeedGenerator()
        self.autoload_options()
        self.context_push({
            "page_title": self.context_get("app_name", os.getenv("APP_NAME", "Silverback")),
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
