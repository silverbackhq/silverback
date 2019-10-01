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


class Prometheus():

    def __init__(self, metrics=[]):
        self.__metrics = metrics

    def set_metrics(self, metrics):
        self.__metrics = metrics

    def push_to_metrics(self, record):
        self.__metrics.append(record)

    def get_plain_metrics(self):
        data = ""
        for metric in self.__metrics:
            if "type" in metric and metric["type"] == "count":
                data += self.__get_count_metric(metric)

        return data

    def __get_count_metric(self, item):
        data = ""
        if "comment" in item:
            data += "# %s\n" % item["comment"]
        data += "%s %d\n" % (item["record"], item["count"])
        return data
