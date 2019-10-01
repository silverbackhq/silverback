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

# Local Library
from .incident import Incident


class IncidentUpdate(models.Model):

    STATUS_CHOICES = (
        ('investigating', 'INVESTIGATING'),
        ('identified', 'IDENTIFIED'),
        ('monitoring', 'MONITORING'),
        ('update', 'UPDATE'),
        ('resolved', 'RESOLVED')
    )

    NOTIFY_CHOICES = (
        ('on', 'ON'),
        ('off', 'OFF')
    )

    incident = models.ForeignKey(
        Incident,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related Incident",
        null=True
    )

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="update", verbose_name="Status")
    notify_subscribers = models.CharField(max_length=50, choices=NOTIFY_CHOICES, default="on", verbose_name="Notify Subscribers")
    total_suscribers = models.IntegerField(default=0, verbose_name="Total Subscribers")
    datetime = models.DateTimeField(verbose_name="Datetime")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        db_table = "app_incident_update"
