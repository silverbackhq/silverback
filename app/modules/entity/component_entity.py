"""
Component Entity Module
"""

from app.models import Component


class Component_Entity():

    def count(self, group_id=None):
        if group_id is None:
            return Component.objects.count()
        else:
            return Component.objects.filter(group_id=group_id).count()

    def clear_group(self, group_id):
        return Component.objects.filter(group_id=group_id).update(group_id=None)
