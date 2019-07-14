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


class TestProfile(TestCase):

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

    def test_profile_update_failure(self):
        self.client.login(username='admin', password="$h12345678H$")
        response = self.client.post(reverse("app.api.private.v1.admin.profile.endpoint"), {
            "action": "_update_profile",
            "first_name": "",
            "last_name": "",
            "username": "",
            "email": "",
            "job_title": "",
            "company": "",
            "address": "",
            "github_url": "",
            "twitter_url": "",
            "facebook_url": ""
        })
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        self.assertEqual(response_body["status"], "failure")

    def test_profile_update_success(self):
        self.client.login(username='admin', password="$h12345678H$")
        response = self.client.post(reverse("app.api.private.v1.admin.profile.endpoint"), {
            "action": "_update_profile",
            "first_name": "Joe",
            "last_name": "Doe",
            "username": "admin",
            "email": "admin@silverback.com",
            "job_title": "Software Engineer",
            "company": "Silverback",
            "address": "",
            "github_url": "",
            "twitter_url": "",
            "facebook_url": ""
        })
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        self.assertEqual(response_body["status"], "success")

    def test_access_token_update_success(self):
        self.client.login(username='admin', password="$h12345678H$")
        response = self.client.post(reverse("app.api.private.v1.admin.profile.endpoint"), {
            "action": "_update_access_token"
        })
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        self.assertEqual(response_body["status"], "success")
        self.assertTrue(response_body["payload"]["token"] != "")

    def test_refresh_token_update_success(self):
        self.client.login(username='admin', password="$h12345678H$")
        response = self.client.post(reverse("app.api.private.v1.admin.profile.endpoint"), {
            "action": "_update_refresh_token"
        })
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        self.assertEqual(response_body["status"], "success")
        self.assertTrue(response_body["payload"]["token"] != "")

    def test_password_update_success(self):
        self.client.login(username='admin', password="$h12345678H$")
        response = self.client.post(reverse("app.api.private.v1.admin.profile.endpoint"), {
            "action": "_update_password",
            "old_password": "$h12345678H$",
            "new_password": "$k12345678H$"
        })
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        self.assertEqual(response_body["status"], "success")
