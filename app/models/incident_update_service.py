"""
Incident Update Notification Model
"""

# Django
from django.db import models

# local Django
from .incident_update import Incident_Update
from .service import Service


class Incident_Update_Service(models.Model):

    incident_update = models.ForeignKey(
        Incident_Update,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related Incident Update",
        null=True
    )

    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related Service",
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
