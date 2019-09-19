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

# Third Party Library
from django.db import models
from django.contrib.auth.models import User

# Local Library
from .task import Task


class Notification(models.Model):

    TYPE_CHOICES = (
        ('pending', 'PENDING'),
        ('failed', 'FAILED'),
        ('passed', 'PASSED'),
        ('error', 'ERROR'),
        ('message', 'MESSAGE')
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related user"
    )

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related Task",
        null=True
    )

    highlight = models.CharField(max_length=200, verbose_name="Highlight")
    notification = models.CharField(max_length=200, verbose_name="Notification")
    url = models.CharField(max_length=200, verbose_name="URL")
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default="message", verbose_name="Type")
    delivered = models.BooleanField(default=False, verbose_name="Delivered")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        db_table = "app_notification"
