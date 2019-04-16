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

    def send_private_success(self, messages, payload={}, correlation_id=""):
        private = {}
        private["status"] = "success"
        private["messages"] = messages
        if len(payload) > 0:
            private["payload"] = payload

        self.__logger.debug(_("App Response: %(response)s {'correlationId':'%(correlationId)s'}\n") % {
            "response": self.__helpers.json_dumps(private),
            "correlationId": correlation_id
        })
        return private

    def send_private_failure(self, messages, payload={}, correlation_id=""):
        private = {}
        private["status"] = "failure"
        private["messages"] = messages
        if len(payload) > 0:
            private["payload"] = payload

        self.__logger.debug(_("App Response: %(response)s {'correlationId':'%(correlationId)s'}\n") % {
            "response": self.__helpers.json_dumps(private),
            "correlationId": correlation_id
        })
        return private

    def send_errors_failure(self, messages, payload={}, correlation_id=""):
        private = {}
        errors = []
        for input_key, error_list in messages.items():
            for error in error_list:
                errors.append({"type": "error", "message": error})
        private["status"] = "failure"
        private["messages"] = errors
        if len(payload) > 0:
            private["payload"] = payload

        self.__logger.debug(_("App Response: %(response)s {'correlationId':'%(correlationId)s'}\n") % {
            "response": self.__helpers.json_dumps(private),
            "correlationId": correlation_id
        })
        return private

    def send_public_success(self, messages, payload={}, correlation_id=""):
        public = {}
        public["status"] = "success"
        public["messages"] = messages
        if len(payload) > 0:
            public["payload"] = payload

        self.__logger.debug(_("App Response: %(response)s {'correlationId':'%(correlationId)s'}\n") % {
            "response": self.__helpers.json_dumps(public),
            "correlationId": correlation_id
        })
        return public

    def send_public_failure(self, messages, payload={}, correlation_id=""):
        public = {}
        public["status"] = "failure"
        public["messages"] = messages
        if len(payload) > 0:
            public["payload"] = payload

        self.__logger.debug(_("App Response: %(response)s {'correlationId':'%(correlationId)s'}\n") % {
            "response": self.__helpers.json_dumps(public),
            "correlationId": correlation_id
        })
        return public

    def send(self, payload={}, correlation_id=""):
        self.__logger.debug(_("App Response: %(response)s {'correlationId':'%(correlationId)s'}\n") % {
            "response": self.__helpers.json_dumps(payload),
            "correlationId": correlation_id
        })
        return payload
