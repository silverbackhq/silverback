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

# Standard Library
import json
import importlib

from django.utils.translation import gettext as _

# Local Library
from app.modules.entity.task_entity import TaskEntity
from app.modules.util.helpers import Helpers


class Task():

    def __init__(self):
        self.__task_entity = TaskEntity()
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

        try:
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
        except Exception as e:
            self.__logger.error(
                _("Error while sending task %(taskName)s with parameters %(parameters)s to workers: %(error)s {'correlationId':'%(correlationId)s'}") % {
                    "taskName": task_name,
                    "parameters": json.dumps(parameters),
                    "error": str(e),
                    "correlationId": parameters["correlation_id"] if "correlation_id" in parameters.keys() else ""
                }
            )

        return False

    def get_many_by_executor(self, executor):
        return self.__task_entity.get_many_by_executor(executor)

    def delete_old_tasks_by_executor(self, executor, minutes):
        return self.__task_entity.delete_old_tasks_by_executor(executor, minutes)
