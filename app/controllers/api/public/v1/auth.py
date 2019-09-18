"""
    Auth API Endpoint
    ~~~~~~~~~~~~~~

    :copyright: silverbackhq
    :license: BSD-3-Clause
"""

# Third Party Library
from django.views import View


class Auth(View):

    def get(self):
        # To get current refresh token
        pass

    def post(self):
        # To Get your new API token in case it is expired
        pass
