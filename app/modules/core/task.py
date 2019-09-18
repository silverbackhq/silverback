"""
    Task Module
    ~~~~~~~~~~~~~~

    :copyright: silverbackhq
    :license: BSD-3-Clause
"""

# Standard Library
import json
import importlib

# Local Library
from app.modules.entity.task_entity import TaskEntity


class Task():

    __task_entity = None

    def __init__(self):
        self.__task_entity = TaskEntity()

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

    def get_many_by_executor(self, executor):
        return self.__task_entity.get_many_by_executor(executor)

    def delete_old_tasks_by_executor(self, executor, minutes):
        return self.__task_entity.delete_old_tasks_by_executor(executor, minutes)
