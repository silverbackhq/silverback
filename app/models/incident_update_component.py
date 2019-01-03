"""
Incident Update Notification Model
"""

# Django
from django.db import models

# local Django
from .incident_update import Incident_Update
from .component import Component


class Incident_Update_Component(models.Model):

    incident_update = models.ForeignKey(
        Incident_Update,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related Incident Update"
    )

    component = models.ForeignKey(
        Component,
        on_delete=models.CASCADE,
        db_index=True,
        verbose_name="Related Component"
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
