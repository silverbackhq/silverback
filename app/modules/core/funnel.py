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


class Funnel():

    __rules = {}
    __request = {}

    def set_rules(self, rules):
        self.__rules = rules

    def set_request(self, request):
        self.__request = request

    def action_needed(self):
        return False

    def fire(self):
        pass

    def _parse(self):
        pass
