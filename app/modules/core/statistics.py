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
from app.modules.entity.task_entity import TaskEntity
from app.modules.entity.user_entity import UserEntity
from app.modules.entity.option_entity import OptionEntity
from app.modules.entity.profile_entity import ProfileEntity


class Statistics():

    __option_entity = None
    __user_entity = None
    __task_entity = None
    __profile_entity = None
    __app_name = ""

    def __init__(self):
        self.__option_entity = OptionEntity()
        self.__user_entity = UserEntity()
        self.__task_entity = TaskEntity()
        self.__profile_entity = ProfileEntity()
        self.__app_name = self.__option_entity.get_value_by_key("app_name").lower()

    def get_all_users(self):
        return {
            "type": "count",
            "record": "%s_all_users" % self.__app_name,
            "count": self.__user_entity.count_all_users(),
            "comment": "Current All Users on System"
        }

    def get_all_profiles(self):
        return {
            "type": "count",
            "record": "%s_all_profiles" % self.__app_name,
            "count": self.__profile_entity.count_all_profiles(),
            "comment": "Current All Profiles on System"
        }

    def get_all_tasks(self):
        return {
            "type": "count",
            "record": "%s_all_tasks" % self.__app_name,
            "count": self.__task_entity.count_all_tasks(),
            "comment": "Current All Tasks on System"
        }
