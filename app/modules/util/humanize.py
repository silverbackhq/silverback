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
from django.utils import timezone
from django.utils.translation import gettext as _


class Humanize():

    def datetime(self, datetime):
        now = timezone.now()
        diff = now - datetime

        second_diff = diff.seconds
        day_diff = diff.days

        if day_diff < 0:
            return ''

        if day_diff == 0:
            if second_diff < 10:
                return _("just now")
            if second_diff < 60:
                return _("%s seconds ago") % str(second_diff)
            if second_diff < 120:
                return _("a minute ago")
            if second_diff < 3600:
                return _("%s minutes ago") % str(round(second_diff / 60))
            if second_diff < 7200:
                return "an hour ago"
            if second_diff < 86400:
                return _("%s hours ago") % str(round(second_diff / 3600))

        if day_diff == 1:
            return "Yesterday"
        if day_diff < 7:
            return _("%s days ago") % str(day_diff)
        if day_diff < 31:
            return _("%s weeks ago") % str(round(day_diff / 7))
        if day_diff < 365:
            return _("%s months ago") % str(round(day_diff / 30))

        return _("%s years ago") % str(round(day_diff / 365))
