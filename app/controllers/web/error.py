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
from django.shortcuts import render
from django.utils.translation import gettext as _

# Local Library
from app.modules.util.helpers import Helpers
from app.controllers.controller import Controller


def handler500(request, exception=None, template_name='templates/500.html'):
    """500 Error Page Controller"""

    helpers = Helpers()
    logger = helpers.get_logger(__name__)

    if exception is not None:
        logger.error("Server Error: %(exception)s" % {
            "exception": exception
        })

    template_name = 'templates/500.html'

    controller = Controller()

    controller.autoload_options()
    controller.context_push({
        "page_title": _("500 · %s") % controller.context_get("app_name", os.getenv("APP_NAME", "Silverback"))
    })

    return render(request, template_name, controller.context_get(), status=500)
