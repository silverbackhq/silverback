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
from app.modules.entity.activity_entity import ActivityEntity


class Activity():

    __activity_entity = None

    def __init__(self):
        self.__activity_entity = ActivityEntity()

    def get_one_by_id(self, id):
        activity = self.__activity_entity.get_one_by_id(id)

        if not activity:
            return False

        return {
            "id": activity.id,
            "activity": activity.activity,
            "user": activity.user
        }

    def track(self, user_id, activity):
        return self.__activity_entity.insert_one({
            "activity": activity,
            "user_id": user_id
        })

    def insert_one(self, activity):
        return self.__activity_entity.insert_one(activity)

    def update_one_by_id(self, id, activity_data):
        return self.__activity_entity.update_one_by_id(id, activity_data)

    def count(self, user_id):
        return self.__activity_entity.count(user_id)

    def count_all(self):
        return self.__activity_entity.count_all()

    def get(self, user_id, offset=None, limit=None):
        return self.__activity_entity.get(user_id, offset, limit)

    def get_all(self, offset=None, limit=None):
        return self.__activity_entity.get_all(offset, limit)

    def delete_one_by_id(self, id):
        return self.__activity_entity.delete_one_by_id(id)
