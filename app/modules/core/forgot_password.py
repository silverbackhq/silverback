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
from django.utils.translation import gettext as _

# Local Library
from app.modules.entity.user_entity import UserEntity
from app.modules.entity.option_entity import OptionEntity
from app.modules.entity.reset_request_entity import ResetRequestEntity
from app.modules.core.task import Task as TaskCore


class ForgotPassword():

    __reset_request_entity = None
    __option_entity = None
    __user_entity = None
    __task_core = None
    __reset_expire_option = 24
    __messages_count_option = 5

    def __init__(self):
        self.__reset_request_entity = ResetRequestEntity()
        self.__option_entity = OptionEntity()
        self.__user_entity = UserEntity()
        self.__task_core = TaskCore()

        messages_count_option = self.__option_entity.get_one_by_key("reset_mails_messages_count")
        reset_expire_option = self.__option_entity.get_one_by_key("reset_mails_expire_after")

        if messages_count_option:
            self.__messages_count_option = int(messages_count_option.value)

        if reset_expire_option:
            self.__reset_expire_option = int(reset_expire_option.value)

    def check_email(self, email):
        return True if self.__user_entity.get_one_by_email(email) is not False else False

    def reset_request_exists(self, email):
        return self.__reset_request_entity.get_one_by_email(email)

    def is_spam(self, request):
        if request.messages_count >= self.__messages_count_option and timezone.now() < request.expire_at:
            return True
        return False

    def update_request(self, request):

        # Delete Old Request
        self.__reset_request_entity.delete_one_by_id(request.id)

        # Create a Fresh Request
        if timezone.now() > request.expire_at:
            return self.create_request(request.email)

        # Create from the Old Request
        request = self.__reset_request_entity.insert_one({
            "email": request.email,
            "expire_at": request.expire_at,
            "messages_count": request.messages_count + 1

        })
        return request.token if request is not False else False

    def create_request(self, email):
        request = self.__reset_request_entity.insert_one({
            "email": email,
            "expire_after": self.__reset_expire_option,
            "messages_count": 0

        })
        return request.token if request is not False else False

    def send_message(self, email, token):

        app_name = self.__option_entity.get_value_by_key("app_name")
        app_email = self.__option_entity.get_value_by_key("app_email")
        app_url = self.__option_entity.get_value_by_key("app_url")
        user = self.__user_entity.get_one_by_email(email)

        return self.__task_core.delay("forgot_password_email", {
            "app_name": app_name,
            "app_email": app_email,
            "app_url": app_url,
            "recipient_list": [email],
            "token": token,
            "subject": _("%s Password Reset") % (app_name),
            "template": "mails/reset_password.html",
            "fail_silently": False
        }, user.id)
