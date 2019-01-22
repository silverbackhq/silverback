"""
Incident Update Model
"""

# Django
from django.db import models

# local Django
from .incident import Incident


class Incident_Update(models.Model):

    STATUS_CHOICES = (
        ('Investigating', 'INVESTIGATING'),
        ('Identified', 'IDENTIFIED'),
        ('Monitoring', 'MONITORING'),
        ('Update', 'UPDATE'),
        ('Resolved', 'RESOLVED')
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

    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="open", verbose_name="Status")
    notify_subscribers = models.CharField(max_length=50, choices=NOTIFY_CHOICES, default="on", verbose_name="Notify Subscribers")
    total_suscribers = models.IntegerField(default=0, verbose_name="Total Subscribers")
    notified_subscribers = models.IntegerField(default=0, verbose_name="Notified Subscribers")
    failed_subscribers = models.IntegerField(default=0, verbose_name="Failed Subscribers")
    datetime = models.DateTimeField(verbose_name="Datetime")
    message = models.TextField(verbose_name="Message")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated at")
