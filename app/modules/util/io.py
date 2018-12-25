"""
Crypto Module
"""

# standard library
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
