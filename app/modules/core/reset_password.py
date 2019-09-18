"""
    Reset Password Module
    ~~~~~~~~~~~~~~

    :copyright: silverbackhq
    :license: BSD-3-Clause
"""

# Third Party Library
from django.utils import timezone

# Local Library
from app.modules.entity.user_entity import UserEntity
from app.modules.entity.reset_request_entity import ResetRequestEntity


class ResetPassword():

    __reset_request_entity = None
    __user_entity = None

    def __init__(self):
        self.__user_entity = UserEntity()
        self.__reset_request_entity = ResetRequestEntity()

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
