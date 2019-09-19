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

# Local Library
from app.modules.core.funnel import Funnel
from app.modules.util.helpers import Helpers


class APIFunnel():

    __helpers = None
    __logger = None
    __funnel = None
    __roles = {}

    def __init__(self, get_response):
        self.__helpers = Helpers()
        self.__funnel = Funnel()
        self.get_response = get_response
        self.__logger = self.__helpers.get_logger(__name__)

    def __call__(self, request):
        self.__funnel.set_rules(self.__roles)
        self.__funnel.set_request(request)

        if self.__funnel.action_needed():
            return self.__funnel.fire()

        response = self.get_response(request)

        return response
