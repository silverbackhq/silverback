"""
Reset Password Module
"""

# Django
from django.utils import timezone

# local Django
from app.modules.util.helpers import Helpers
from app.modules.entity.user_entity import User_Entity
from app.modules.entity.reset_request_entity import Reset_Request_Entity


class Reset_Password():

    __reset_request_entity = None
    __helpers = None
    __user_entity = None

    def __init__(self):
        self.__helpers = Helpers()
        self.__user_entity = User_Entity()
        self.__reset_request_entity = Reset_Request_Entity()

    def check_token(self, token):
        request = self.__reset_request_entity.get_one_by_token(token)
        if request is not False and timezone.now() < request.expire_at:
            return True
        return False

    def reset_password(self, token, new_password):
        request = self.__reset_request_entity.get_one_by_token(token)
        if request is not False and timezone.now() < request.expire_at:
            return self.__user_entity.update_password_by_email(request.email, new_password)
        return False

    def delete_reset_request(self, token):
        return self.__reset_request_entity.delete_one_by_token(token)
