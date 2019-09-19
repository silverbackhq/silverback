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
import json
import logging
import random
import string
import uuid
from pprint import pprint
from datetime import timedelta

# Third Party Library
import pytz
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import activate


class Helpers():

    __loggers = {}

    def slugify(self, text, allow_unicode=False):
        return slugify(text, allow_unicode=allow_unicode)

    def get_logger(self, name=__name__):
        if name in self.__loggers:
            return self.__loggers[name]
        self.__loggers[name] = logging.getLogger(name)
        return self.__loggers[name]

    def switch_language(self, language):
        activate(language)

    def get_request_data(self, data_bag, predicted):
        request_data = {}

        for key, default in predicted.items():
            request_data[key] = data_bag[key] if key in data_bag else default

        return request_data

    def json_dumps(self, data):
        return json.dumps(data)

    def json_loads(self, data):
        return json.loads(data)

    def dump_var(self, var):
        pprint(var)

    def substr(self, haystack, needle):
        return False if haystack.find(needle) < 0 else True

    def time_after(self, interval):
        datetime = timezone.now()
        for key, value in interval.items():
            if key == "microseconds":
                datetime += timedelta(microseconds=value)
            elif key == "milliseconds":
                datetime += timedelta(milliseconds=value)
            elif key == "seconds":
                datetime += timedelta(seconds=value)
            elif key == "minutes":
                datetime += timedelta(minutes=value)
            elif key == "hours":
                datetime += timedelta(hours=value)
            elif key == "days":
                datetime += timedelta(days=value)
            elif key == "weeks":
                datetime += timedelta(weeks=value)
            elif key == "months":
                datetime += timedelta(days=value * 30)
            elif key == "years":
                datetime += timedelta(days=value * 360)
        return datetime

    def random_generator(self, size=6, chars=string.ascii_lowercase + string.digits):
        return ''.join(random.choice(chars) for x in range(size))

    def generate_uuid(self):
        return str(uuid.uuid4())

    def tz_aware_datetime(self, dt_str):
        dt = parse_datetime(dt_str)
        return pytz.timezone(os.getenv("APP_TIMEZONE", "UTC")).localize(dt, is_dst=None)
