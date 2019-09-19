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


class Task(models.Model):

    STATUS_CHOICES = (
        ('pending', 'PENDING'),
        ('failed', 'FAILED'),
        ('passed', 'PASSED'),
        ('error', 'ERROR')
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related user",
        null=True
    )

    uuid = models.CharField(max_length=200, verbose_name="UUID")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending", verbose_name="Status")
    executor = models.CharField(max_length=200, verbose_name="Executor")
    parameters = models.TextField(verbose_name="Parameters")
    result = models.TextField(verbose_name="Result")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        db_table = "app_task"
