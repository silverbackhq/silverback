"""
Component Module
"""

# Local Library
from app.modules.entity.component_entity import Component_Entity
from app.modules.entity.component_group_entity import Component_Group_Entity


class Component():

    __component_group_entity = None
    __component_entity = None

    def __init__(self):
        self.__component_group_entity = Component_Group_Entity()
        self.__component_entity = Component_Entity()

    def get_one_by_id(self, id):
        component = self.__component_entity.get_one_by_id(id)

        if not component:
            return False

        return {
            "id": component.id,
            "name": component.name,
            "description": component.description,
            "uptime": component.uptime,
            "group_id": "" if component.group is None else component.group.id,
            "group_name": "" if component.group is None else component.group.name
        }

    def insert_one(self, component):
        return self.__component_entity.insert_one(component)

    def update_one_by_id(self, id, component_data):
        return self.__component_entity.update_one_by_id(id, component_data)

    def count_all(self):
        return self.__component_entity.count_all()

    def get_all(self, offset=None, limit=None):
        return self.__component_entity.get_all(offset, limit)

    def get_all_groups(self):
        return self.__component_group_entity.get_all()

    def delete_one_by_id(self, id):
        return self.__component_entity.delete_one_by_id(id)
