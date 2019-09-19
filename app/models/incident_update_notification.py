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
from .incident_update import IncidentUpdate
from .subscriber import Subscriber


class IncidentUpdateNotification(models.Model):

    STATUS_CHOICES = (
        ('pending', 'PENDING'),
        ('failed', 'FAILED'),
        ('success', 'SUCCESS')
    )

    incident_update = models.ForeignKey(
        IncidentUpdate,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related Incident Update",
        null=True
    )

    subscriber = models.ForeignKey(
        Subscriber,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related Subscriber",
        null=True
    )

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="pending", verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        db_table = "app_incident_update_notification"
