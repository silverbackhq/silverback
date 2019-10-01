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
from django.core.validators import validate_email
from django.contrib.auth import authenticate, login

# Local Library
from app.modules.entity.option_entity import OptionEntity
from app.modules.entity.user_entity import UserEntity


class Login():

    def __init__(self):
        self.__option_entity = OptionEntity()
        self.__user_entity = UserEntity()

    def is_authenticated(self, request):
        if request.user and request.user.is_authenticated:
            return True
        else:
            return False

    def authenticate(self, username_email, password, request=None, with_login=True):
        is_email = False
        try:
            is_email = True if validate_email(username_email) is None else False
        except Exception:
            is_email = False
        if is_email:
            user = self.__user_entity.get_one_by_email(username_email)
            if user is not False and user.check_password(password) is True:
                if with_login:
                    self.login(request, user)
                return True
            else:
                return False
        else:
            user = authenticate(request=request, username=username_email, password=password)
            if user is not None:
                if with_login:
                    self.login(request, user)
                return True
            else:
                return False

    def login(self, request, user):
        return login(request, user)
