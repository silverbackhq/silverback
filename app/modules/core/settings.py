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
from app.modules.entity.option_entity import OptionEntity


class Settings():

    def __init__(self):
        self.__option_entity = OptionEntity()

    def update_options(self, options):
        status = True
        for key, value in options.items():
            status &= self.__option_entity.update_value_by_key(key, value)
        return status

    def get_value_by_key(self, key, default=""):
        return self.__option_entity.get_value_by_key(key, default)
