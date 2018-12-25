"""
Register Module
"""

# local Django
from app.modules.util.helpers import Helpers
from app.modules.entity.option_entity import Option_Entity
from app.modules.entity.user_entity import User_Entity
from app.modules.entity.notification_entity import Notification_Entity
from app.modules.core.acl import ACL


class Register():

    __notification_entity = None
    __option_entity = None
    __user_entity = None
    __helpers = None
    __logger = None
    __acl = None

    def __init__(self):
        self.__acl = ACL()
        self.__option_entity = Option_Entity()
        self.__user_entity = User_Entity()
        self.__helpers = Helpers()
        self.__notification_entity = Notification_Entity()
        self.__logger = self.__helpers.get_logger(__name__)

    def username_used(self, username):
        return False if self.__user_entity.get_one_by_username(username) is False else True

    def email_used(self, email):
        return False if self.__user_entity.get_one_by_email(email) is False else True

    def create_user(self, user_data):
        status = True

        user = self.__user_entity.insert_one({
            "username": user_data["username"],
            "email": user_data["email"],
            "password": user_data["password"],
            "first_name": user_data["first_name"],
            "last_name": user_data["last_name"],
            "is_superuser": False,
            "is_active": True,
            "is_staff": False
        })

        if user is not False:
            self.__acl.add_role_to_user("normal_user", user.id)

        status &= (user is not False)

        return status
