"""
Test Home Controller
"""

# Third Party Library
from django.test import TestCase
from django.shortcuts import reverse

# Local Library
from app.tests.testing_base import TestingBase


class TestHome(TestCase):

    def setUp(self):
        tb = TestingBase()
        tb.uninstall()
        tb.install({
            "app_name": "Silverback",
            "app_email": "hello@silverback.com",
            "app_url": "http://silverback.com",
            "admin_username": "admin",
            "admin_email": "admin@silverback.com",
            "admin_password": "$h12345678H$"
        })

    def tearDown(self):
        tb = TestingBase()
        tb.uninstall()

    def test_get(self):
        response = self.client.get(reverse("app.web.status_page_index"))
        self.assertEqual(response.status_code, 200)
