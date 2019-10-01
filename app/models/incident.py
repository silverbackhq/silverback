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


class Incident(models.Model):

    STATUS_CHOICES = (
        ('open', 'OPEN'),
        ('closed', 'CLOSED')
    )

    name = models.CharField(max_length=200, verbose_name="Name")
    uri = models.CharField(max_length=50, verbose_name="URI", unique=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="open", verbose_name="Status")
    datetime = models.DateTimeField(verbose_name="Datetime")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        db_table = "app_incident"
