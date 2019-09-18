"""
    Incident Update Notification Model
    ~~~~~~~~~~~~~~

    :copyright: silverbackhq
    :license: BSD-3-Clause
"""

# Third Party Library
from django.db import models

# Local Library
from .incident_update import IncidentUpdate
from .component import Component


class IncidentUpdateComponent(models.Model):

    TYPES_CHOICES = (
        ('operational', 'OPERATIONAL'),
        ('degraded_performance', 'DEGRADED_PERFORMANCE'),
        ('partial_outage', 'PARTIAL_OUTAGE'),
        ('major_outage', 'MAJOR_OUTAGE'),
        ('maintenance', 'MAINTENANCE')
    )

    incident_update = models.ForeignKey(
        IncidentUpdate,
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

    type = models.CharField(max_length=50, choices=TYPES_CHOICES, default="operational", verbose_name="Type")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")

    class Meta:
        db_table = "app_incident_update_component"
