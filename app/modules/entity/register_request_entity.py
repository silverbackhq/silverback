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

# Standard Library
from datetime import datetime
from datetime import timedelta

# Third Party Library
from django.utils import timezone
from django.utils.crypto import get_random_string

# Local Library
from app.models import RegisterRequest


class RegisterRequestEntity():

    def gererate_token(self):
        """Generate a Token"""
        token = get_random_string(length=50)
        while self.get_one_by_token(token) is not False:
            token = get_random_string(length=50)
        return token

    def insert_one(self, request):
        """Insert a New Register Request"""
        if self.get_one_by_email(request["email"]) is not False:
            return False

        request = RegisterRequest(
            email=request["email"],
            token=request["token"] if "token" in request else self.gererate_token(),
            payload=request["payload"],
            expire_at=request["expire_at"] if "expire_at" in request else timezone.now() + timedelta(hours=int(request["expire_after"]))
        )

        request.save()
        return False if request.pk is None else request

    def insert_many(self, requests):
        """Insert Many Register Requests"""
        status = True
        for request in requests:
            status &= True if self.insert_one(request) is not False else False
        return status

    def get_one_by_id(self, id):
        """Get Register Request By ID"""
        try:
            register_request = RegisterRequest.objects.get(pk=id)
            return False if register_request.pk is None else register_request
        except Exception:
            return False

    def get_one_by_email(self, email):
        """Get Register Request By Email"""
        try:
            register_request = RegisterRequest.objects.get(email=email)
            return False if register_request.pk is None else register_request
        except Exception:
            return False

    def get_one_by_token(self, token):
        """Get Register Request By Token"""
        try:
            register_request = RegisterRequest.objects.get(token=token)
            return False if register_request.pk is None else register_request
        except Exception:
            return False

    def clear_expired_tokens(self):
        """Clear all Expired Tokens"""
        RegisterRequest.objects.filter(expire_at__lt=datetime.now()).delete()

    def delete_one_by_id(self, id):
        """Delete Register Request By ID"""
        request = self.get_one_by_id(id)
        if request is not False:
            count, deleted = request.delete()
            return True if count > 0 else False
        return False

    def delete_one_by_token(self, token):
        """Delete Register Request By Token"""
        request = self.get_one_by_token(token)
        if request is not False:
            count, deleted = request.delete()
            return True if count > 0 else False
        return False

    def delete_one_by_email(self, email):
        """Delete Register Request By Email"""
        request = self.get_one_by_email(email)
        if request is not False:
            count, deleted = request.delete()
            return True if count > 0 else False
        return False
