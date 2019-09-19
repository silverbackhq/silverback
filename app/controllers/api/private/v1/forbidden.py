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
from django.http import JsonResponse
from django.utils.translation import gettext as _

# Local Library
from app.modules.core.response import Response


def csrf_failure(request, reason=""):
    correlation_id = request.META["X-Correlation-ID"] if "X-Correlation-ID" in request.META else ""
    response = Response()
    return JsonResponse(response.send_private_failure([{
        "type": "error",
        "message": _("Error! Access forbidden due to invalid CSRF token.")
    }], {}, correlation_id))
