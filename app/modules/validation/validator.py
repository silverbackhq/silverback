"""
Validator Module
"""

# standard library
import re
import uuid

# Django
from django.core.signing import Signer
from django.core.validators import validate_email
from django.core.validators import validate_ipv4_address
from django.core.validators import validate_ipv6_address
from django.core.validators import validate_ipv46_address
from django.core.validators import URLValidator


class Validator():

    __input = None

    def set_input(self, input_value):
        self.__input = input_value

    def empty(self):
        return self.__input == ''

    def not_empty(self):
        return not self.__input.replace(' ', '') == ''

    def length_between(self, from_length, to_length):
        if to_length > len(self.__input) > from_length:
            return True
        else:
            return False

    def min_length(self, min_length):
        if len(self.__input) >= min_length:
            return True
        else:
            return False

    def max_length(self, max_length):
        if len(self.__input) <= max_length:
            return True
        else:
            return False

    def exact_length(self, exact_length):
        if len(self.__input) == exact_length:
            return True
        else:
            return False

    def greater_than(self, number):
        if int(self.__input) > number:
            return True
        else:
            return False

    def greater_than_equal(self, number):
        if int(self.__input) >= number:
            return True
        else:
            return False

    def less_than(self, number):
        if int(self.__input) < number:
            return True
        else:
            return False

    def less_than_equal(self, number):
        if int(self.__input) <= number:
            return True
        else:
            return False

    def equal(self, number):
        if int(self.__input) == number:
            return True
        else:
            return False

    def same_as(self, text):
        if self.__input == text:
            return True
        else:
            return False

    def any_of(self, options):
        return self.__input in options

    def all_of(self, options):
        if not len(options) == len(self.__input):
            return False
        status = True
        for item in self.__input:
            status &= item in options
        return status

    def none_of(self, options):
        return self.__input not in options

    def alpha(self):
        if not isinstance(self.__input, (str)):
            return False
        return self.__input.isalpha()

    def alpha_numeric(self):
        if not isinstance(self.__input, (str)):
            return False
        return self.__input.isalnum()

    def password(self):
        if re.search("[a-z]", self.__input) is None:
            return False
        if re.search("[A-Z]", self.__input) is None:
            return False
        if re.search("[0-9]", self.__input) is None:
            return False
        if not re.search(r"^[a-zA-Z0-9]*$", self.__input) is None:
            return False
        return True

    def names(self):
        return (re.search(r'[^a-zA-Z\s\-\']', self.__input) is None)

    def username_or_email(self):
        return self.email() or self.alpha_numeric()

    def digit(self):
        if not isinstance(self.__input, (str)):
            return False
        return self.__input.isdigit()

    def email(self):
        try:
            return True if validate_email(self.__input) is None else False
        except Exception:
            return False

    def emails(self, sep=','):
        status = True
        for email in self.__input.split(sep):
            try:
                status &= True if validate_email(self.__input) is None else False
            except Exception:
                status &= False
        return status

    def url(self, protocols=['http', 'https']):
        validate = URLValidator(protocols)
        try:
            return True if validate(self.__input) is None else False
        except Exception:
            return False

    def ip(self, formats=['ipv4', 'ipv6']):
        if 'ipv4' in formats and 'ipv6' in formats:
            return self.ipv46()
        elif 'ipv6' in formats:
            return self.ipv6()
        elif 'ipv4' in formats:
            return self.ipv4()
        else:
            return False

    def ipv4(self):
        try:
            return True if validate_ipv4_address(self.__input) is None else False
        except Exception:
            return False

    def ipv6(self):
        try:
            return True if validate_ipv6_address(self.__input) is None else False
        except Exception:
            return False

    def ipv46(self):
        try:
            return True if validate_ipv46_address(self.__input) is None else False
        except Exception:
            return False

    def uuid(self):
        try:
            uuid.UUID(self.__input)
            return True
        except Exception:
            return False

    def matches(self, regex, flags=0):
        if isinstance(regex, (str)):
            regex = re.compile(regex, flags)

        return bool(regex.match(self.__input))

    def token(self):
        signer = Signer()
        try:
            original = signer.unsign(self.__input)
        except Exception:
            return False

        return True if original != "" else False

    def optional(self):
        return self.__input == ""

    def numeric(self):
        regex = re.compile(r'^[0-9]+$')
        return bool(regex.match(self.__input))

    def host_slug(self):
        regex = re.compile(r'^[a-z0-9-_]+$')
        return bool(regex.match(self.__input))

    def host_name(self):
        regex = re.compile(r'^[a-zA-Z0-9-_\s]+$')
        return bool(regex.match(self.__input))

    def host_server(self):
        return True

    def tls_certificate(self):
        return True
