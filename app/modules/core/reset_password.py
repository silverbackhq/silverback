# Copyright 2019 Silverbackhq
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
