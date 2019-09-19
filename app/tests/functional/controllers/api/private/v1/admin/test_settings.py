# Copyright 2019 Silverbackhq
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Standard Library
import json

# Third Party Library
from django.test import TestCase
from django.shortcuts import reverse

# Local Library
from app.tests.testing_base import TestingBase


class TestSettings(TestCase):

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

    def test_not_auth(self):
        response = self.client.post(reverse("app.api.private.v1.admin.settings.endpoint"), {
            "app_name": "Silverback",
            "app_email": "hello@silverback.com",
            "app_url": "http://silverback.com",
            "app_description": "A Status and Incident Communication Tool.",
            "google_analytics_account": "GA-123",
            "reset_mails_messages_count": "5",
            "reset_mails_expire_after": "5",
            "access_tokens_expire_after": "5",
            "prometheus_token": "PRO-123",
            "newrelic_api_key": "NR-123"
        })
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        self.assertEqual(response_body["status"], "failure")

    def test_failure(self):
        self.client.login(username='admin', password="$h12345678H$")
        response = self.client.post(reverse("app.api.private.v1.admin.settings.endpoint"), {
            "app_name": "",
            "app_email": "",
            "app_url": "",
            "app_description": "",
            "google_analytics_account": "",
            "reset_mails_messages_count": "1",
            "reset_mails_expire_after": "1",
            "access_tokens_expire_after": "1",
            "prometheus_token": "",
            "newrelic_api_key": ""
        })
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        self.assertEqual(response_body["status"], "failure")

    def test_success(self):
        self.client.login(username='admin', password="$h12345678H$")
        response = self.client.post(reverse("app.api.private.v1.admin.settings.endpoint"), {
            "app_name": "Silverback",
            "app_email": "hello@silverback.com",
            "app_url": "http://silverback.com",
            "app_description": "A Status and Incident Communication Tool.",
            "google_analytics_account": "GA-123",
            "reset_mails_messages_count": "5",
            "reset_mails_expire_after": "5",
            "access_tokens_expire_after": "5",
            "prometheus_token": "PRO-123",
            "newrelic_api_key": "NR-123"
        })
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        self.assertEqual(response_body["status"], "success")
