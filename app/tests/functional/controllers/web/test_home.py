"""
Test Error Controller
"""

# Third Party Library
from django.test import TestCase
from django.shortcuts import reverse


class TestHome(TestCase):

    def test_get(self):
        response = self.client.get(reverse("app.web.status_page_index"))
        self.assertTrue(response.status_code in (200, 302))
