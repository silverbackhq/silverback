"""
Health Module
"""

import os
import redis
from django.utils.translation import gettext as _


class Health():

    OK = "OK"
    NOT_OK = "NOT_OK"

    def check_db(self):
        errors = []
        return errors

    def check_io(self):
        errors = []
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
