"""
Health Module
"""

import os
from django.utils.translation import gettext as _
from app.modules.entity.option_entity import Option_Entity
from app.settings.info import APP_ROOT
from app.modules.core.task import Task as Task_Core


class Health():

    OK = "OK"
    NOT_OK = "NOT_OK"
    MIN_OPTIONS = 6

    __io_directories = [
        "/storage/logs",
        "/storage/app/private",
        "/storage/app/public",
        "/storage/mails",
        "/storage/database"
    ]

    def check_db(self):
        errors = []

        try:
            option_entity = Option_Entity()
            if option_entity.count() < Health.MIN_OPTIONS:
                errors.append(_("Application not installed yet."))
        except Exception as e:
            errors.append(_("Error Connecting to database: %(error)s") % {"error": str(e)})

        return errors

    def check_io(self):
        errors = []

        for directory in self.__io_directories:
            status = os.access(APP_ROOT + directory, os.F_OK)
            status &= os.access(APP_ROOT + directory, os.R_OK)
            status &= os.access(APP_ROOT + directory, os.W_OK)
            if not status:
                errors.append(_("Error: directory %(directory)s not writable") % {"directory": APP_ROOT + directory})

        return errors

    def check_workers(self):
        errors = []
        task_core = Task_Core()
        last_task = task_core.get_one_by_executor("app.tasks.ping.ping")

        if last_task and last_task.status != "passed":
            errors.append(_("Error: celery workers not performing well or down."))

        task_core.delete_tasks_by_executor("app.tasks.ping.ping")

        try:
            task_core.delay("ping", {
                "text": "PONG"
            }, None)
        except Exception as e:
            errors.append(_("Error while creating a ping task: %(error)s") % {"error": str(e)})

        return errors
