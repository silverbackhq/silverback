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


class TestStatusSubscribe(TestCase):

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

    def test_subscribe_failure(self):
        response = self.client.post(reverse("app.api.private.v1.status_subscribe.endpoint"), {
            "type": "",
            "email": "",
            "phone": "",
            "endpoint": "",
            "auth_token": ""
        })
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        self.assertEqual(response_body["status"], "failure")

    def test_subscribe_success01(self):
        response = self.client.post(reverse("app.api.private.v1.status_subscribe.endpoint"), {
            "type": "email",
            "email": "hello@silverbackhq.com",
            "phone": "",
            "endpoint": "",
            "auth_token": ""
        })
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        self.assertEqual(response_body["status"], "success")

    def test_subscribe_success02(self):
        response = self.client.post(reverse("app.api.private.v1.status_subscribe.endpoint"), {
            "type": "phone",
            "email": "",
            "phone": "00312345678",
            "endpoint": "",
            "auth_token": ""
        })
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        self.assertEqual(response_body["status"], "success")

    def test_subscribe_success03(self):
        response = self.client.post(reverse("app.api.private.v1.status_subscribe.endpoint"), {
            "type": "endpoint",
            "email": "hello@silverbackhq.com",
            "phone": "",
            "endpoint": "http://silverbackhq.org/hook",
            "auth_token": "12345678"
        })
        self.assertEqual(response.status_code, 200)
        response_body = json.loads(response.content)
        self.assertEqual(response_body["status"], "success")
