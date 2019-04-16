"""
Health Module
"""

import os
import redis
from django.utils.translation import gettext as _
from app.modules.entity.option_entity import Option_Entity
from app.settings.info import APP_ROOT


class Health():

    OK = "OK"
    NOT_OK = "NOT_OK"
    MIN_OPTIONS = 6

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

        directories = [
            "/storage/logs",
            "/storage/app/private",
            "/storage/app/public",
            "/storage/mails",
            "/storage/database"
        ]

        for directory in directories:
            status = os.access(APP_ROOT + directory, os.F_OK)
            status &= os.access(APP_ROOT + directory, os.R_OK)
            status &= os.access(APP_ROOT + directory, os.W_OK)
            if not status:
                errors.append(_("Error: directory %(directory)s not writable") % {"directory": APP_ROOT + directory})

        return errors

    def check_workers(self):
        errors = []
        return errors

    def check_cache(self):
        errors = []

        try:
            connection = redis.Redis(
                host=os.getenv("REDIS_HOST"),
                port=os.getenv("REDIS_PORT"),
                db=os.getenv("REDIS_DB"),
                password=None if os.getenv("REDIS_PASSWORD") == "" else os.getenv("REDIS_PASSWORD")
            )
            connection.ping()
        except Exception as e:
            errors.append(_("Error Connecting to redis server: %(error)s") % {"error": str(e)})

        return errors
