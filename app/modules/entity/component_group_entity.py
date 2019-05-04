"""
Component Group Entity Module
"""

# Local Library
from app.models import Component_Group


class Component_Group_Entity():

    def insert_one(self, group):

        new_group = Component_Group()

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
            group = Component_Group.objects.get(id=group_id)
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
        return Component_Group.objects.count()

    def get_all(self, offset=None, limit=None):
        if offset is None or limit is None:
            return Component_Group.objects.order_by('-created_at')
        return Component_Group.objects.order_by('-created_at')[offset:limit+offset]
