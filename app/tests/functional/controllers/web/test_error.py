"""
Test Error Controller
"""

from django.test import TestCase


class TestError(TestCase):

    def test_get(self):
        response = self.client.get('/500')
        self.assertEqual(response.status_code, 200)
