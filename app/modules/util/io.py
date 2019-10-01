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


class Directory():

    def __init__(self):
        pass

    def create(self, dirs):
        return os.makedirs(dirs)

    def delete(self, path, dirname, recursive=False):
        pass

    def exists(self, dir):
        return os.path.isdir(dir)


class File():

    def __init__(self):
        pass

    def write(self, file, content):
        with open(file, 'w') as f:
            f.write(content)

    def delete(self, path, filename, recursive=False):
        pass

    def exists(self, file):
        return os.path.isfile(file)

    def rename(self, path, old_filename, new_filename):
        pass

    def read(self, file):
        contents = ""
        with open(file, 'r') as f:
            for line in f.readlines():
                contents += line
        return contents
