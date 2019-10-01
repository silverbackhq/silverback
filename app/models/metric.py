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


class Metric(models.Model):

    SOURCE_CHOICES = (
        ('newrelic', 'NEW_RELIC'),
        ('librato', 'LIBRATO'),
        ('datadog', 'DATADOG'),
        ('pingdom', 'PINGDOM')
    )

    title = models.CharField(max_length=150, verbose_name="Title")
    description = models.CharField(max_length=200, verbose_name="Description")
    x_axis = models.CharField(max_length=100, verbose_name="x_axis")
    y_axis = models.CharField(max_length=100, verbose_name="y_axis")
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default="newrelic", verbose_name="Source")
    data = models.TextField(verbose_name="Data")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        db_table = "app_metric"
