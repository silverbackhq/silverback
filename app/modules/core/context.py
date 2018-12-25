"""
Context Module
"""

# local Django
from app.settings.info import AUTHOR
from app.settings.info import COPYRIGHT
from app.settings.info import LICENSE
from app.settings.info import VERSION
from app.settings.info import MAINTAINER
from app.settings.info import EMAIL
from app.settings.info import STATUS
from app.settings.info import REPO_URL
from app.settings.info import AUTHOR_URL
from app.settings.info import RELEASES
from app.settings.info import SUPPORT_URL
from app.modules.util.helpers import Helpers
from app.modules.util.gravatar import Gravatar
from app.modules.entity.option_entity import Option_Entity
from app.modules.entity.user_entity import User_Entity


class Context():

    __data = {}
    __option_entity = None
    __user_entity = None
    __helpers = None
    __logger = None

    def __init__(self):

        self.__option_entity = Option_Entity()
        self.__user_entity = User_Entity()
        self.__helpers = Helpers()

        self.__data["AUTHOR"] = AUTHOR
        self.__data["COPYRIGHT"] = COPYRIGHT
        self.__data["LICENSE"] = LICENSE
        self.__data["VERSION"] = VERSION
        self.__data["MAINTAINER"] = MAINTAINER
        self.__data["EMAIL"] = EMAIL
        self.__data["STATUS"] = STATUS
        self.__data["REPO_URL"] = REPO_URL
        self.__data["AUTHOR_URL"] = AUTHOR_URL
        self.__data["RELEASES"] = RELEASES
        self.__data["SUPPORT_URL"] = SUPPORT_URL
        self.__logger = self.__helpers.get_logger(__name__)

    def push(self, new_data):
        self.__data.update(new_data)

    def load_options(self, options):
        options_to_load = {}
        for key in options.keys():
            options_to_load[key] = options[key]
            if key not in self.__data.keys():
                self.__data[key] = options[key]

        if len(options_to_load.keys()) > 0:
            new_options = self.__option_entity.get_many_by_keys(options_to_load.keys())
            for option in new_options:
                self.__data[option.key] = option.value

    def autoload_options(self):
        options = self.__option_entity.get_many_by_autoload(True)
        for option in options:
            self.__data[option.key] = option.value

    def autoload_user(self, user_id):
        user_data = {
            "user_first_name": "",
            "user_last_name": "",
            "user_username": "",
            "user_email": "",
            "user_avatar": ""
        }

        if user_id is not None:
            user = self.__user_entity.get_one_by_id(user_id)
            if user is not False:
                user_data["user_first_name"] = user.first_name
                user_data["user_last_name"] = user.last_name
                user_data["user_username"] = user.username
                user_data["user_email"] = user.email
                user_data["user_avatar"] = Gravatar(user.email).get_image()

        self.__data.update(user_data)

    def get(self, key=None, default=None):
        if key is not None:
            return self.__data[key] if key in self.__data else default
        return self.__data
