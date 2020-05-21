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
import logging

# Local Library
from app.modules.util.helpers import Helpers


class Correlation():

    def __init__(self, get_response):
        self.__helpers = Helpers()
        self.get_response = get_response

    def __call__(self, request):
        request.META["X-Correlation-ID"] = self.__helpers.generate_uuid()

        response = self.get_response(request)

        return response


class CorrelationFilter(logging.Filter):

    def __init__(self, correlation_id=""):
        self.correlation_id = correlation_id

    def filter(self, record):
        if not hasattr(record, 'correlation_id'):
            record.correlation_id = self.correlation_id
        return True
