"""
Sanitizer Module
"""


class Sanitizer():

    __input = None
    __sinput = None

    def set_input(self, input_value):
        self.__input = input_value

    def set_sinput(self, sinput_value):
        self.__sinput = sinput_value

    def get_sinput(self):
        return self.__sinput

    def get_input(self):
        return self.__input

    def is_exact(self):
        return self.__input == self.__sinput and len(self.__input) == len(self.__sinput)

    def strip(self, chars=''):
        if not isinstance(self.__input, (str)):
            self.__sinput = str(self.__input)
        else:
            self.__sinput = self.__input

        if len(chars) > 0:
            self.__sinput = self.__sinput.strip(chars)
        else:
            self.__sinput = self.__sinput.strip()

        return self.__sinput

    def lstrip(self, chars=''):
        if not isinstance(self.__input, (str)):
            self.__sinput = str(self.__input)
        else:
            self.__sinput = self.__input

        if len(chars) > 0:
            self.__sinput = self.__sinput.lstrip(chars)
        else:
            self.__sinput = self.__sinput.lstrip()

        return self.__sinput

    def rstrip(self, chars=''):
        if not isinstance(self.__input, (str)):
            self.__sinput = str(self.__input)
        else:
            self.__sinput = self.__input

        if len(chars) > 0:
            self.__sinput = self.__sinput.rstrip(chars)
        else:
            self.__sinput = self.__sinput.rstrip()

        return self.__sinput

    def escape(self, chars=['&', '"', '\'', '>', '<']):
        html_escape_table = {
            "&": "&amp;" if '&' in chars else '&',
            '"': "&quot;" if '"' in chars else '"',
            "'": "&apos;" if '\'' in chars else '\'',
            ">": "&gt;" if '>' in chars else '>',
            "<": "&lt;" if '<' in chars else '<',
        }

        if not isinstance(self.__input, (str)):
            self.__sinput = str(self.__input)
        else:
            self.__sinput = self.__input

        self.__sinput = "".join(html_escape_table.get(c, c) for c in self.__sinput)
        return self.__sinput
