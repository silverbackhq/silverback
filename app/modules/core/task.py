"""
Task Module
"""

# standard library
import json
import importlib

# local Django
from app.modules.util.helpers import Helpers
from app.modules.entity.task_entity import Task_Entity


class Task():

    __task_entity = None
    __helpers = None
    __logger = None

    def __init__(self):
        self.__task_entity = Task_Entity()
        self.__helpers = Helpers()
        self.__logger = self.__helpers.get_logger(__name__)

    def get_task_with_uuid(self, uuid):
        return self.__task_entity.get_one_by_uuid(uuid)

    def update_task_with_uuid(self, uuid, task):
        return self.__task_entity.update_one_by_uuid(uuid, task)

    def create_task(self, task):
        return self.__task_entity.insert_one(task)

    def delay(self, task_name, parameters, user_id):
        tasks_module = importlib.import_module("app.tasks")
        task_object = getattr(tasks_module, task_name)

        task_result = task_object.delay(**parameters)

        if task_result.task_id != "":

            return self.create_task({
                "uuid": task_result.task_id,
                "status": "pending",
                "executor": task_object.name,
                "parameters": json.dumps(parameters),
                "result": '{}',
                "user_id": user_id
            })

        return False
