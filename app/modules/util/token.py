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
from random import randrange

# Third Party Library
from django.core.signing import Signer
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password


class Token():

    def gererate_random(self, length=50):
        return get_random_string(length)

    def generate_hash(self, length=50, rand_length=20):
        generated_hash = make_password(self.gererate_random(rand_length))
        return generated_hash[0:length]

    def generate_token(self, rand_length=15):
        generated_rand = self.gererate_random(randrange(rand_length, rand_length + rand_length))
        signer = Signer()
        return signer.sign(generated_rand)

    def validate_token(self, token):
        signer = Signer()
        try:
            original = signer.unsign(token)
        except Exception:
            return False

        return True if original != "" else False
