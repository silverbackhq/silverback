"""
Incident Update Model
"""

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
