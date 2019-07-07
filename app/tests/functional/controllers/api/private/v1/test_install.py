"""
Test Install Controller
"""

# Standard Library
import json

# Third Party Library
from django.test import TestCase
from django.shortcuts import reverse


class TestInstall(TestCase):

    def test_failure(self):
        response = self.client.post(reverse("app.api.private.v1.install.endpoint"))
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        self.assertEqual(response_body["status"], "failure")
        self.assertTrue(len(response_body["messages"]) > 0)

    def test_success(self):
        response = self.client.post(reverse("app.api.private.v1.install.endpoint"),  {
            "app_name": "Silverback",
            "app_email": "hello@silverback.com",
            "app_url": "http://silverback.com",
            "admin_username": "admin",
            "admin_email": "admin@silverback.com",
            "admin_password": "$h12345678H$"
        })
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        self.assertEqual(response_body["status"], "success")
