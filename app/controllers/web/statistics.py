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

# Third Party Library
from django.views import View
from django.http import HttpResponse
from django.http import Http404

# Local Library
from app.modules.service.prometheus import Prometheus
from app.modules.core.decorators import redirect_if_not_installed
from app.modules.core.decorators import protect_metric_with_auth_key
from app.modules.core.statistics import Statistics as StatisticsModule


class Statistics(View):

    __prometheus = None
    __statistics = None
    __correlation_id = None

    @redirect_if_not_installed
    @protect_metric_with_auth_key
    def get(self, request, type):

        self.__correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
        self.__prometheus = Prometheus()
        self.__statistics = StatisticsModule()

        if type not in ("prometheus"):
            raise Http404("Page not found.")

        if type == "prometheus":

            self.__prometheus.set_metrics([
                self.__statistics.get_all_users(),
                self.__statistics.get_all_profiles(),
                self.__statistics.get_all_tasks()
            ])

            return HttpResponse(self.__prometheus.get_plain_metrics(), content_type='text/plain')
