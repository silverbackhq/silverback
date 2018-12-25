"""
Sign Module
"""

# standard library
from random import randrange

# Django
from django.core.signing import Signer
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password


class Token():

    def gererate_random(self, length=50):
        return get_random_string(length)

    def generate_hash(self, length=50, rand_length=20):
        generated_hash = make_password(self.gererate_random(rand_length))
        return generated_hash[0:length]

    def generate_token(self, rand_length=15):
        generated_rand = self.gererate_random(randrange(rand_length, rand_length + rand_length))
        signer = Signer()
        return signer.sign(generated_rand)

    def validate_token(self, token):
        signer = Signer()
        try:
            original = signer.unsign(token)
        except Exception:
            return False

        return True if original != "" else False
