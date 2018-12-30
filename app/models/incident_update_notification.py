"""
Incident Update Notification Model
"""

# Django
from django.db import models

# local Django
from .incident_update import Incident_Update
from .subscriber import Subscriber


class Incident_Update_Notification(models.Model):

    incident_update = models.ForeignKey(
        Incident_Update,
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

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")