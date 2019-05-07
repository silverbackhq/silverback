"""
User Module
"""

# Standard Library
import json

# Third Party Library
from django.utils import timezone
from django.utils.translation import gettext as _

# Local Library
from app.modules.core.acl import ACL
from app.modules.core.task import Task as Task_Core
from app.modules.entity.user_entity import User_Entity
from app.modules.entity.option_entity import Option_Entity
from app.modules.entity.notification_entity import Notification_Entity
from app.modules.entity.register_request_entity import Register_Request_Entity


class User():

    __notification_entity = None
    __option_entity = None
    __user_entity = None
    __acl = None
    __register_request_entity = None
    __task_core = None
    __register_expire_option = 24

    def __init__(self):
        self.__acl = ACL()
        self.__option_entity = Option_Entity()
        self.__user_entity = User_Entity()
        self.__notification_entity = Notification_Entity()
        self.__register_request_entity = Register_Request_Entity()
        self.__task_core = Task_Core()

    def username_used(self, username):
        return False if self.__user_entity.get_one_by_username(username) is False else True

    def email_used(self, email):
        return False if self.__user_entity.get_one_by_email(email) is False else True

    def username_used_elsewhere(self, user_id, username):
        user = self.__user_entity.get_one_by_username(username)

        if user is False or user.id == user_id:
            return False

        return True

    def email_used_elsewhere(self, user_id, email):
        user = self.__user_entity.get_one_by_email(email)

        if user is False or user.id == user_id:
            return False

        return True

    def get_one_by_id(self, id):
        user = self.__user_entity.get_one_by_id(id)

        if not user:
            return False

        return {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "role": "admin" if user.is_superuser else "user",
        }

    def insert_one(self, user):
        return self.__user_entity.insert_one(user)

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

    def update_one_by_id(self, id, user_data):
        return self.__user_entity.update_one_by_id(id, user_data)

    def check_register_request(self, token):
        request = self.__register_request_entity.get_one_by_token(token)
        if request is not False and timezone.now() < request.expire_at:
            return True
        return False

    def get_register_request_by_token(self, token):
        return self.__register_request_entity.get_one_by_token(token)

    def delete_register_request_by_token(self, token):
        return self.__register_request_entity.delete_one_by_token(token)

    def delete_register_request_by_email(self, email):
        return self.__register_request_entity.delete_one_by_email(email)

    def create_register_request(self, email, role):
        request = self.__register_request_entity.insert_one({
            "email": email,
            "payload": json.dumps({"role": role}),
            "expire_after": self.__register_expire_option

        })
        return request.token if request is not False else False

    def send_register_request_message(self, email, token):

        app_name = self.__option_entity.get_value_by_key("app_name")
        app_email = self.__option_entity.get_value_by_key("app_email")
        app_url = self.__option_entity.get_value_by_key("app_url")

        return self.__task_core.delay("register_request_email", {
            "app_name": app_name,
            "app_email": app_email,
            "app_url": app_url,
            "recipient_list": [email],
            "token": token,
            "subject": _("%s Signup Invitation") % (app_name),
            "template": "mails/register_invitation.html",
            "fail_silently": False
        }, 1)

    def count_all(self):
        return self.__user_entity.count_all()

    def get_all(self, offset=None, limit=None):
        return self.__user_entity.get_all(offset, limit)

    def delete_one_by_id(self, id):
        return self.__user_entity.delete_one_by_id(id)
