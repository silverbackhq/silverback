"""
Response Module
"""

# Django
from django.utils.translation import gettext as _

# local Django
from app.modules.util.helpers import Helpers


class Response():

    __helpers = None
    __logger = None

    def __init__(self):
        self.__helpers = Helpers()
        self.__logger = self.__helpers.get_logger(__name__)

    def send_private_success(self, messages, payload={}):
        __private = {}
        __private["status"] = "success"
        __private["messages"] = messages
        if len(payload) > 0:
            __private["payload"] = payload

        self.__logger.debug(_("App Response: ") + self.__helpers.json_dumps(__private) + "\n")
        return __private

    def send_private_failure(self, messages, payload={}):
        __private = {}
        __private["status"] = "failure"
        __private["messages"] = messages
        if len(payload) > 0:
            __private["payload"] = payload

        self.__logger.debug(_("App Response: ") + self.__helpers.json_dumps(__private) + "\n")
        return __private

    def send_public_success(self, messages, payload={}):
        __public = {}
        __public["status"] = "success"
        __public["messages"] = messages
        if len(payload) > 0:
            __public["payload"] = payload

        self.__logger.debug(_("App Response: ") + self.__helpers.json_dumps(__public) + "\n")
        return __public

    def send_public_failure(self, messages, payload={}):
        __public = {}
        __public["status"] = "failure"
        __public["messages"] = messages
        if len(payload) > 0:
            __public["payload"] = payload

        self.__logger.debug(_("App Response: ") + self.__helpers.json_dumps(__public) + "\n")
        return __public
