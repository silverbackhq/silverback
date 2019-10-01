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
from django.core.management import utils
from django.core.management.base import BaseCommand, CommandError

# Local Library
from app.settings.info import APP_ROOT
from app.settings.info import VERSION


class Command(BaseCommand):

    help = "Play around with Silverback Application!"

    available = [
        "info",
        "update_app_key",
        "update_env"
    ]

    def add_arguments(self, parser):
        """Config Command Args"""
        parser.add_argument('command', type=str, nargs='+', help='Available commands are %s' % ", ".join(self.available))

    def handle(self, *args, **options):
        """Command Handle"""
        if len(options['command']) == 0 or options['command'][0] not in self.available:
            raise CommandError('Command Does not exist! Please use one of the following: python manage.py silverback [%s]' % ", ".join(self.available))

        if options['command'][0] == "update_env" and (len(options['command']) != 2 or not options['command'][1].find("=") > 1):
            raise CommandError('Error! Invalid command format.')

        if options['command'][0] == "info":
            self.stdout.write(self.style.SUCCESS('Current Version is: %s' % VERSION))
        elif options['command'][0] == "update_app_key":
            self.__refresh_app_key()
        elif options['command'][0] == "update_env":
            env_data = options['command'][1].split("=")
            self.__update_env_var(env_data[0], env_data[1])

    def __update_env_var(self, key, value):
        """Update Env Variable"""
        if not os.path.isfile(os.path.join(APP_ROOT, '.env')):
            self.stdout.write(self.style.ERROR('Error! .env File is Missing.'))
            return None

        with open(os.path.join(APP_ROOT, '.env'), 'r') as file:
            data = file.readlines()

        i = 0
        for item in data:
            if item.startswith(key + "="):
                self.stdout.write(self.style.SUCCESS('%s updated to: %s' % (key, value)))
                data[i] = "%s=%s\n" % (key, value)
            i += 1

        with open(os.path.join(APP_ROOT, '.env'), 'w') as file:
            file.writelines(data)

    def __refresh_app_key(self):
        """Refresh APP Key"""
        if not os.path.isfile(os.path.join(APP_ROOT, '.env')):
            self.stdout.write(self.style.ERROR('Error! .env File is Missing.'))
            return None

        with open(os.path.join(APP_ROOT, '.env'), 'r') as file:
            data = file.readlines()

        i = 0
        for value in data:
            if value.startswith("APP_KEY="):
                key = utils.get_random_secret_key()
                self.stdout.write(self.style.SUCCESS('App Key Updated to: %s' % key))
                data[i] = "APP_KEY=%s\n" % key
            i += 1

        with open(os.path.join(APP_ROOT, '.env'), 'w') as file:
            file.writelines(data)
