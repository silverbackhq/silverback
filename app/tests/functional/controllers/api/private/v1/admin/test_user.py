"""
Test Profile Controller
"""

# Standard Library
import json

# Third Party Library
from django.test import TestCase
from django.shortcuts import reverse

# Local Library
from app.tests.testing_base import TestingBase


class TestUser(TestCase):

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

    def test_create_users(self):
        self.client.login(username='admin', password="$h12345678H$")
        response = self.client.post(reverse("app.api.private.v1.admin.users.endpoint"), {
            "invitation": "1",
            "first_name": "Joe",
            "last_name": "Doe",
            "username": "admin01",
            "role": "user",
            "email": "admin01@silverback.com",
            "password": "$l12345678L$"
        })
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        self.assertEqual(response_body["status"], "success")

    def test_get_users(self):
        self.client.login(username='admin', password="$h12345678H$")
        response = self.client.get(reverse("app.api.private.v1.admin.users.endpoint"), {
            "offset": "0",
            "limit": "100"
        })
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        self.assertEqual(response_body["status"], "success")
        self.assertEqual(response_body["payload"]["users"][0]["id"], 1)
        self.assertEqual(response_body["payload"]["users"][0]["username"], "admin")
        self.assertEqual(response_body["payload"]["users"][0]["first_name"], "")
        self.assertEqual(response_body["payload"]["users"][0]["last_name"], "")
        self.assertEqual(response_body["payload"]["users"][0]["email"], "admin@silverback.com")
        self.assertEqual(response_body["payload"]["users"][0]["role"], "Admin")
        self.assertEqual(response_body["payload"]["users"][0]["edit_url"], "/admin/users/edit/1")
        self.assertEqual(response_body["payload"]["users"][0]["delete_url"], "/api/private/v1/admin/user/1")
        self.assertEqual(response_body["payload"]["metadata"]["offset"], 0)
        self.assertEqual(response_body["payload"]["metadata"]["limit"], 100)
        self.assertEqual(response_body["payload"]["metadata"]["count"], 1)

    def test_update_users_01(self):
        self.client.login(username='admin', password="$h12345678H$")
        response = self.client.post(reverse("app.api.private.v1.admin.user.endpoint", args=[1]), {
            "first_name": "Joe",
            "last_name": "Doe",
            "username": "admin",
            "role": "admin",
            "email": "admin@silverback.com",
            "update_password": "",
            "password": ""
        })
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        self.assertEqual(response_body["status"], "success")

    def test_update_users_02(self):
        self.client.login(username='admin', password="$h12345678H$")
        response = self.client.post(reverse("app.api.private.v1.admin.user.endpoint", args=[1]), {
            "first_name": "Joe",
            "last_name": "Doe",
            "username": "admin",
            "role": "admin",
            "email": "admin@silverback.com",
            "update_password": "1",
            "password": "$k12345678K$"
        })
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        self.assertEqual(response_body["status"], "success")

    def test_delete_users01(self):
        self.client.login(username='admin', password="$h12345678H$")
        response = self.client.delete(reverse("app.api.private.v1.admin.user.endpoint", args=[1]))
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        self.assertEqual(response_body["status"], "failure")
