"""
Component Entity Module
"""

from app.models import Component
from app.models import Component_Group


class Component_Entity():

    def insert_one(self, component):

        new_component = Component()

        if "name" in component:
            new_component.name = component["name"]

        if "description" in component:
            new_component.description = component["description"]

        if "uptime" in component:
            new_component.uptime = component["uptime"]

        if "group_id" in component:
            new_component.group = None if component["group_id"] is None else Component_Group.objects.get(pk=component["group_id"])

        new_component.save()
        return False if new_component.pk is None else new_component

    def update_one_by_id(self, id, component_data):
        component = self.get_one_by_id(id)

        if component is not False:
            if "name" in component_data:
                component.name = component_data["name"]

            if "description" in component_data:
                component.description = component_data["description"]

            if "uptime" in component_data:
                component.uptime = component_data["uptime"]

            if "group_id" in component_data:
                component.group = None if component_data["group_id"] is None else Component_Group.objects.get(pk=component_data["group_id"])

            component.save()
            return True
        return False

    def get_one_by_id(self, component_id):
        try:
            component = Component.objects.get(id=component_id)
            return False if component.pk is None else component
        except Exception:
            return False

    def delete_one_by_id(self, id):
        component = self.get_one_by_id(id)
        if component is not False:
            count, deleted = component.delete()
            return True if count > 0 else False
        return False

    def count_all(self):
        return Component.objects.count()

    def get_all(self, offset=None, limit=None):
        if offset is None or limit is None:
            return Component.objects.order_by('-created_at')

        return Component.objects.order_by('-created_at')[offset:limit+offset]

    def count(self, group_id=None):
        if group_id is None:
            return Component.objects.count()
        else:
            return Component.objects.filter(group_id=group_id).count()

    def clear_group(self, group_id):
        return Component.objects.filter(group_id=group_id).update(group_id=None)
