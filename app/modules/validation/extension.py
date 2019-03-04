"""
Validation Extensions
"""

# standard library
import re
import uuid

from pyvalitron.validator import Validator

# Django
from django.core.signing import Signer
from django.core.validators import validate_email
from django.core.validators import validate_ipv4_address
from django.core.validators import validate_ipv6_address
from django.core.validators import validate_ipv46_address
from django.core.validators import URLValidator


class ExtraRules(Validator):

    def sv_password(self):
        if re.search("[a-z]", self._input) is None:
            return False
        if re.search("[A-Z]", self._input) is None:
            return False
        if re.search("[0-9]", self._input) is None:
            return False
        if not re.search(r"^[a-zA-Z0-9]*$", self._input) is None:
            return False
        return True

    def sv_names(self):
        return (re.search(r'[^a-zA-Z\s\-\']', str(self._input)) is None)

    def sv_username_or_email(self):
        return self.email() or self.alpha_numeric()

    def sv_email(self):
        try:
            return True if validate_email(self._input) is None else False
        except Exception:
            return False

    def sv_emails(self, sep=','):
        status = True
        for email in self._input.split(sep):
            try:
                status &= True if validate_email(self._input) is None else False
            except Exception:
                status &= False
        return status

    def sv_url(self, protocols=['http', 'https']):
        validate = URLValidator(protocols)
        try:
            return True if validate(self._input) is None else False
        except Exception:
            return False

    def sv_ip(self, formats=['ipv4', 'ipv6']):
        if 'ipv4' in formats and 'ipv6' in formats:
            return self.sv_ipv46()
        elif 'ipv6' in formats:
            return self.sv_ipv6()
        elif 'ipv4' in formats:
            return self.sv_ipv4()
        else:
            return False

    def sv_ipv4(self):
        try:
            return True if validate_ipv4_address(self._input) is None else False
        except Exception:
            return False

    def sv_ipv6(self):
        try:
            return True if validate_ipv6_address(self._input) is None else False
        except Exception:
            return False

    def sv_ipv46(self):
        try:
            return True if validate_ipv46_address(self._input) is None else False
        except Exception:
            return False

    def sv_token(self):
        signer = Signer()
        try:
            original = signer.unsign(self._input)
        except Exception:
            return False

        return True if original != "" else False

    def sv_numeric(self):
        regex = re.compile(r'^[0-9]+$')
        return bool(regex.match(self._input))

    def sv_host_slug(self):
        regex = re.compile(r'^[a-z0-9-_]+$')
        return bool(regex.match(self._input))

    def sv_host_name(self):
        regex = re.compile(r'^[a-zA-Z0-9-_\s]+$')
        return bool(regex.match(self._input))

    def sv_host_server(self):
        return True

    def sv_tls_certificate(self):
        return True

    def optional(self):
        return self._input == ""
