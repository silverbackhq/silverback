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
from app.models import ComponentGroup


class ComponentGroupEntity():

    def insert_one(self, group):

        new_group = ComponentGroup()

        if "name" in group:
            new_group.name = group["name"]

        if "description" in group:
            new_group.description = group["description"]

        if "uptime" in group:
            new_group.uptime = group["uptime"]

        new_group.save()
        return False if new_group.pk is None else new_group

    def update_one_by_id(self, id, group_data):
        group = self.get_one_by_id(id)

        if group is not False:
            if "name" in group_data:
                group.name = group_data["name"]

            if "description" in group_data:
                group.description = group_data["description"]

            if "uptime" in group_data:
                group.uptime = group_data["uptime"]

            group.save()
            return True
        return False

    def get_one_by_id(self, group_id):
        try:
            group = ComponentGroup.objects.get(id=group_id)
            return False if group.pk is None else group
        except Exception:
            return False

    def get_one_by_name(self, name):
        try:
            group = ComponentGroup.objects.get(name=name)
            return False if group.pk is None else group
        except Exception:
            return False

    def delete_one_by_id(self, id):
        group = self.get_one_by_id(id)
        if group is not False:
            count, deleted = group.delete()
            return True if count > 0 else False
        return False

    def count_all(self):
        return ComponentGroup.objects.count()

    def get_all(self, offset=None, limit=None):
        if offset is None or limit is None:
            return ComponentGroup.objects.order_by('-created_at')
        return ComponentGroup.objects.order_by('-created_at')[offset:limit+offset]
