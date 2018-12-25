"""
Auth API Endpoint
"""

# Django
from django.views import View


class Auth(View):

    def get(self):
        # To get current refresh token
        pass

    def post(self):
        # To Get your new API token in case it is expired
        pass
