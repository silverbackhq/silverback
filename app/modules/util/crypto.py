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
import os

# Third Party Library
from dotenv import load_dotenv
from cryptography.fernet import Fernet

# Local Library
from app.settings.info import APP_ROOT


class Crypto():

    __app_crypto_key = None

    def __init__(self):
        load_dotenv(dotenv_path=os.path.join(APP_ROOT, ".env"))
        self.__app_crypto_key = os.getenv("APP_CRYPTO_KEY")
        self.__app_crypto_key = self.__app_crypto_key if type(self.__app_crypto_key) is bytes else str.encode(self.__app_crypto_key)

    def encrypt(self, data, token=""):
        data = data if type(data) is bytes else str.encode(data)
        token = token if type(token) is bytes else str.encode(token)

        real_token = Fernet(self.__app_crypto_key).decrypt(token)
        return Fernet(real_token).encrypt(data).decode("utf-8")

    def decrypt(self, encrypted_data, token=""):
        encrypted_data = encrypted_data if type(encrypted_data) is bytes else str.encode(encrypted_data)
        token = token if type(token) is bytes else str.encode(token)
        real_token = Fernet(self.__app_crypto_key).decrypt(token)
        return Fernet(real_token).decrypt(encrypted_data).decode("utf-8")

    def get_token(self):
        real_token = Fernet.generate_key()
        return Fernet(self.__app_crypto_key).encrypt(real_token).decode("utf-8")
