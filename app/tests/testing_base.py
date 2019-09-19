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

from app.modules.core.install import Install as Install_Module


class TestingBase():

    __install_module = None

    def __init__(self):
        self.__install_module = Install_Module()

    def login(self):
        pass

    def install(self, data):

        if self.__install_module.is_installed():
            return True

        self.__install_module.set_app_data(
            data["app_name"],
            data["app_email"],
            data["app_url"]
        )
        self.__install_module.set_admin_data(
            data["admin_username"],
            data["admin_email"],
            data["admin_password"]
        )

        return self.__install_module.install()

    def uninstall(self):
        return self.__install_module.uninstall()
