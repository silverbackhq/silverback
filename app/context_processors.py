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

# Local Library
from app.modules.entity.option_entity import OptionEntity
from app.modules.core.constants import Constants


def globals(request):

    option_entity = OptionEntity()

    return {
        "google_account": option_entity.get_value_by_key("google_analytics_account", ""),
        "app_timezone": os.getenv("APP_TIMEZONE", "UTC"),
        "activate_notifications": os.getenv("ACTIVATE_NOTIFICATIONS", "false") == "true",
        "constants": Constants(),
    }
